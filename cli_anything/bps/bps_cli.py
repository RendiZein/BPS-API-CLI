"""
Main Click entry point for BPS Agent-Native CLI Suite.
Provides command groups for session management, readiness status, metadata discovery,
and dynamic data retrieval with strict stream separation.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import click

from . import __version__
from .core.api import BPSClient, load_env
from .core.audit import audit_topic, inspect_variable
from .core.cache import BPSCache
from .core.preview import PreviewProtocol
from .core.session import SessionStore
from .utils.error_handler import BPSAuthError, BPSError, handle_error
from .utils.stream import ascii_safe, emit_output, supports_interactive_prompt


def _get_client(ctx: click.Context) -> BPSClient:
    """Instantiate BPSClient using context options or environment."""
    load_env()
    api_key = ctx.obj.get("api_key") or os.environ.get("BPS_API_KEY")
    domain = ctx.obj.get("domain")

    # If domain not explicitly passed, inspect session store
    if not domain:
        store = SessionStore(ctx.obj.get("session"))
        state = store.load()
        domain = state.domain or "0000"

    timeout = ctx.obj.get("timeout", 25)
    return BPSClient(api_key=api_key, default_domain=domain, timeout=timeout)


def common_options(func):
    """Decorator allowing --json to be passed either before or after subcommands."""
    @click.option("--json", "cmd_json", is_flag=True, default=False, help="Emit machine-readable JSON to stdout.")
    def wrapper(*args, cmd_json: bool = False, **kwargs):
        ctx = click.get_current_context(silent=True)
        if ctx and cmd_json:
            ctx.obj["json"] = True
        return func(*args, **kwargs)
    return wrapper


@click.group(invoke_without_command=True)
@click.option("--json", "json_output", is_flag=True, help="Emit machine-readable JSON to stdout.")
@click.option("--session", "session_path", type=click.Path(dir_okay=False), default=None, help="Path to session JSON file.")
@click.option("--domain", default=None, help="Override active BPS domain ID (e.g. 0000 for National, 3500 for Jatim).")
@click.option("--timeout", type=int, default=25, help="HTTP timeout in seconds.")
@click.option("--key", "api_key", default=None, help="Explicit BPS API key override.")
@click.version_option(__version__, prog_name="bps")
@click.pass_context
def cli(
    ctx: click.Context,
    json_output: bool,
    session_path: Optional[str],
    domain: Optional[str],
    timeout: int,
    api_key: Optional[str],
) -> None:
    """BPS (Badan Pusat Statistik) Agent-Native CLI Suite."""
    ctx.ensure_object(dict)
    ctx.obj.update({
        "json": json_output,
        "session": session_path,
        "domain": domain,
        "timeout": timeout,
        "api_key": api_key,
    })

    if ctx.invoked_subcommand is None:
        ctx.invoke(repl)


# =============================================================================
# REPL Command
# =============================================================================
@cli.command()
@click.pass_context
def repl(ctx: click.Context) -> None:
    """Start interactive REPL mode (or plain fallback if piped)."""
    if supports_interactive_prompt():
        try:
            from .utils.repl_skin import ReplSkin
            skin = ReplSkin("bps", version=__version__)
            skin.run(ctx)
            return
        except ImportError:
            pass

    # Plain text REPL fallback for piped streams or Windows non-tty
    sys.stdout.write(f"BPS Agent CLI v{__version__} (Plain REPL Mode)\nType 'exit' or 'quit' to leave.\n\n")
    sys.stdout.flush()
    while True:
        try:
            sys.stdout.write("bps> ")
            sys.stdout.flush()
            line = sys.stdin.readline()
            if not line:
                break
            cmd = line.strip()
            if not cmd:
                continue
            if cmd in {"exit", "quit", "q"}:
                break
            # Split and invoke command safely
            args = cmd.split()
            try:
                cli.main(args=args, standalone_mode=False, obj=ctx.obj)
            except Exception as e:
                sys.stderr.write(f"Command error: {e}\n")
        except (KeyboardInterrupt, EOFError):
            break


# =============================================================================
# Readiness & Health Status
# =============================================================================
@cli.command("status")
@common_options
@click.pass_context
@handle_error
def status_cmd(ctx: click.Context) -> None:
    """Check BPS API connection readiness, latency, and key validity."""
    start_time = time.time()
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()

    try:
        client = _get_client(ctx)
        # Test ping against default domain
        client.get_domains(domain_type="prov")
        latency_ms = int((time.time() - start_time) * 1000)
        payload = {
            "ok": True,
            "status": "ONLINE",
            "api_version": client.version,
            "latency_ms": latency_ms,
            "key_configured": bool(client.api_key),
            "active_session": {
                "domain": state.domain,
                "domain_name": state.domain_name,
                "name": state.session_name,
            },
        }
    except Exception as exc:
        payload = {
            "ok": False,
            "status": "OFFLINE_OR_ERROR",
            "error": str(exc),
            "key_configured": bool(os.environ.get("BPS_API_KEY")),
            "active_session": {
                "domain": state.domain,
                "domain_name": state.domain_name,
            },
        }

    emit_output(payload, as_json=ctx.obj.get("json", False))


# =============================================================================
# Session Command Group
# =============================================================================
@cli.group("session")
def session_group():
    """Manage research session state and undo/redo stacks."""
    pass


@session_group.command("init")
@click.option("--domain", default="0000", help="Initial domain ID.")
@click.option("--name", default="default", help="Session label.")
@common_options
@click.pass_context
@handle_error
def session_init(ctx: click.Context, domain: str, name: str):
    """Initialize a research session state."""
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()
    store.record_snapshot(state, "session_init", {"domain": domain, "name": name})

    state.domain = domain
    state.session_name = name
    store.save(state)
    store.log_trajectory("init", f"bps session init --domain {domain} --name {name}")

    payload = {"ok": True, "message": f"Session initialized: {name}", "domain": domain}
    emit_output(payload, as_json=ctx.obj.get("json", False))


@session_group.command("status")
@common_options
@click.pass_context
@handle_error
def session_status(ctx: click.Context):
    """View active session state and snapshot stack depth."""
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()
    payload = {
        "ok": True,
        "domain": state.domain,
        "domain_name": state.domain_name,
        "subject_id": state.subject_id,
        "var_id": state.var_id,
        "session_name": state.session_name,
        "history_depth": len(state.history),
        "future_depth": len(state.future),
    }
    emit_output(payload, as_json=ctx.obj.get("json", False))


@session_group.command("set-domain")
@click.argument("domain_id")
@common_options
@click.pass_context
@handle_error
def session_set_domain(ctx: click.Context, domain_id: str):
    """Set active domain ID for the current session."""
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()
    store.record_snapshot(state, "set_domain", {"old_domain": state.domain, "new_domain": domain_id})

    state.domain = str(domain_id)
    store.save(state)
    store.log_trajectory("set_domain", f"bps session set-domain {domain_id}")

    payload = {"ok": True, "domain": state.domain, "message": f"Active domain set to {domain_id}"}
    emit_output(payload, as_json=ctx.obj.get("json", False))


@session_group.command("undo")
@common_options
@click.pass_context
@handle_error
def session_undo(ctx: click.Context):
    """Undo the last session action."""
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()
    restored = store.undo(state)
    store.log_trajectory("undo", "bps session undo")

    payload = {"ok": True, "message": "Undone to previous state.", "restored_state": restored}
    emit_output(payload, as_json=ctx.obj.get("json", False))


@session_group.command("redo")
@common_options
@click.pass_context
@handle_error
def session_redo(ctx: click.Context):
    """Redo the last undone session action."""
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()
    restored = store.redo(state)
    store.log_trajectory("redo", "bps session redo")

    payload = {"ok": True, "message": "Re-applied state.", "restored_state": restored}
    emit_output(payload, as_json=ctx.obj.get("json", False))


@session_group.command("reset")
@common_options
@click.pass_context
@handle_error
def session_reset(ctx: click.Context):
    """Reset session state to default national domain (0000)."""
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()
    store.record_snapshot(state, "reset")

    state.domain = "0000"
    state.domain_name = "Nasional"
    state.subject_id = None
    state.var_id = None
    store.save(state)
    store.log_trajectory("reset", "bps session reset")

    payload = {"ok": True, "message": "Session reset to default national domain (0000)."}
    emit_output(payload, as_json=ctx.obj.get("json", False))


# =============================================================================
# Indicators Command
# =============================================================================
@cli.command("indicators")
@click.option("--page", type=int, default=1, help="Page number.")
@common_options
@click.pass_context
@handle_error
def indicators_cmd(ctx: click.Context, page: int):
    """Fetch Strategic Macroeconomic Indicators (PDRB, Inflation, Poverty, Unemployment, HDI)."""
    client = _get_client(ctx)
    pagination, items = client.get_indicators(page=page)
    payload = {
        "ok": True,
        "domain": client.default_domain,
        "pagination": pagination,
        "count": len(items),
        "data": items,
    }
    emit_output(payload, as_json=ctx.obj.get("json", False))


# =============================================================================
# Subject & Variable Discovery
# =============================================================================
@cli.command("subject")
@click.option("--keyword", default=None, help="Search filter keyword.")
@click.option("--page", type=int, default=1, help="Page number.")
@common_options
@click.pass_context
@handle_error
def subject_cmd(ctx: click.Context, keyword: Optional[str], page: int):
    """List or search statistical subjects."""
    client = _get_client(ctx)
    pagination, items = client.get_subjects(page=page)
    if keyword:
        kw = keyword.lower()
        items = [s for s in items if kw in str(s.get("title", "")).lower() or kw in str(s.get("sub_id", "")).lower()]

    payload = {
        "ok": True,
        "domain": client.default_domain,
        "count": len(items),
        "pagination": pagination,
        "data": items,
    }
    emit_output(payload, as_json=ctx.obj.get("json", False))


@cli.command("variable")
@click.option("--subject", type=int, default=None, help="Filter by subject ID.")
@click.option("--keyword", default=None, help="Search filter keyword.")
@click.option("--page", type=int, default=1, help="Page number.")
@common_options
@click.pass_context
@handle_error
def variable_cmd(ctx: click.Context, subject: Optional[int], keyword: Optional[str], page: int):
    """List statistical variables under a subject."""
    client = _get_client(ctx)
    pagination, items = client.get_variables(subject=subject, page=page)
    if keyword:
        kw = keyword.lower()
        items = [v for v in items if kw in str(v.get("title", "")).lower() or kw in str(v.get("var_id", "")).lower()]

    payload = {
        "ok": True,
        "domain": client.default_domain,
        "subject_id": subject,
        "count": len(items),
        "pagination": pagination,
        "data": items,
    }
    emit_output(payload, as_json=ctx.obj.get("json", False))


# =============================================================================
# Audit & Inspect Commands (Research Availability Engine)
# =============================================================================
@cli.command("audit")
@click.option("--topic", required=True, help="Research topic or keyword (e.g. 'kemiskinan', 'inflasi').")
@click.option("--domain", "domain_query", default=None, help="Target domain ID or name (e.g. '3500', 'Jawa Timur').")
@common_options
@click.pass_context
@handle_error
def audit_cmd(ctx: click.Context, topic: str, domain_query: Optional[str]):
    """Audit BPS data availability, time series depth, and research feasibility for a topic."""
    client = _get_client(ctx)
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()

    target_domain = domain_query or ctx.obj.get("domain") or state.domain or "0000"
    cache = BPSCache()

    result = audit_topic(client=client, topic=topic, domain_query=target_domain, cache=cache)
    store.log_trajectory("audit", f"bps audit --topic \"{topic}\" --domain {target_domain}")

    emit_output(result, as_json=ctx.obj.get("json", False))


@cli.command("inspect")
@click.option("--var", "var_id", type=int, required=True, help="Variable ID to inspect.")
@click.option("--domain", default=None, help="Domain ID override.")
@common_options
@click.pass_context
@handle_error
def inspect_cmd(ctx: click.Context, var_id: int, domain: Optional[str]):
    """Inspect detailed dimensions (vervar, turvar, periods) of a specific variable."""
    client = _get_client(ctx)
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()

    target_domain = domain or ctx.obj.get("domain") or state.domain or "0000"
    result = inspect_variable(client=client, var_id=var_id, domain=target_domain)
    store.log_trajectory("inspect", f"bps inspect --var {var_id} --domain {target_domain}")

    emit_output(result, as_json=ctx.obj.get("json", False))


# =============================================================================
# Local Cache Commands
# =============================================================================
@cli.group("cache")
def cache_group():
    """Manage local SQLite metadata cache for domains and subjects."""
    pass


@cache_group.command("sync")
@common_options
@click.pass_context
@handle_error
def cache_sync(ctx: click.Context):
    """Sync BPS domains and national subjects to local SQLite cache."""
    client = _get_client(ctx)
    cache = BPSCache()

    sys.stderr.write("Fetching domains from BPS API...\n")
    domains = client.get_domains(domain_type="all")
    d_count = cache.sync_domains(domains)

    sys.stderr.write("Fetching national subjects from BPS API...\n")
    _, subjects = client.get_subjects(domain="0000", page=1)
    s_count = cache.sync_subjects("0000", subjects)

    payload = {
        "ok": True,
        "message": "Local cache synced successfully.",
        "domains_cached": d_count,
        "subjects_cached": s_count,
    }
    emit_output(payload, as_json=ctx.obj.get("json", False))


@cache_group.command("status")
@common_options
@click.pass_context
@handle_error
def cache_status(ctx: click.Context):
    """View local SQLite cache size and sync status."""
    cache = BPSCache()
    payload = {"ok": True, **cache.status()}
    emit_output(payload, as_json=ctx.obj.get("json", False))


@cache_group.command("clear")
@common_options
@click.pass_context
@handle_error
def cache_clear(ctx: click.Context):
    """Clear local SQLite metadata cache."""
    cache = BPSCache()
    cache.clear()
    payload = {"ok": True, "message": "Local cache cleared."}
    emit_output(payload, as_json=ctx.obj.get("json", False))


# =============================================================================
# Preview & Fetch Commands (Preview Protocol & Safety Dry-Run)
# =============================================================================
@cli.command("preview")
@click.option("--var", "var_id", type=int, required=True, help="Variable ID.")
@click.option("--th", "th_id", required=True, help="Period/Year ID (th).")
@click.option("--domain", default=None, help="Domain ID override.")
@click.option("--refresh", is_flag=True, default=False, help="Bypass cache and force re-fetch.")
@common_options
@click.pass_context
@handle_error
def preview_cmd(ctx: click.Context, var_id: int, th_id: str, domain: Optional[str], refresh: bool):
    """Generate or retrieve a SHA-256 cached data preview bundle (summary.json)."""
    client = _get_client(ctx)
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()

    target_domain = domain or ctx.obj.get("domain") or state.domain or "0000"
    protocol = PreviewProtocol()

    result = protocol.generate_preview_bundle(
        client=client,
        var_id=var_id,
        th_id=th_id,
        domain=target_domain,
        force_refresh=refresh,
    )
    store.log_trajectory("preview", f"bps preview --var {var_id} --th {th_id} --domain {target_domain}", bundle_id=result.get("bundle_id"))

    emit_output(result, as_json=ctx.obj.get("json", False))


@cli.command("fetch")
@click.option("--var", "var_id", type=int, required=True, help="Variable ID.")
@click.option("--th", "th_id", required=True, help="Period/Year ID (th).")
@click.option("--domain", default=None, help="Domain ID override.")
@click.option("--format", "export_format", type=click.Choice(["csv", "json"], case_sensitive=False), default="csv", help="Output format.")
@click.option("--output", "output_path", type=click.Path(dir_okay=False), default=None, help="Target file path to save data.")
@click.option("--dry-run", is_flag=True, default=False, help="Calculate request quota and rate-limit without executing.")
@common_options
@click.pass_context
@handle_error
def fetch_cmd(
    ctx: click.Context,
    var_id: int,
    th_id: str,
    domain: Optional[str],
    export_format: str,
    output_path: Optional[str],
    dry_run: bool,
):
    """Fetch complete dynamic dataset with optional CSV/JSON export and safety dry-run."""
    client = _get_client(ctx)
    store = SessionStore(ctx.obj.get("session"))
    state = store.load()

    target_domain = domain or ctx.obj.get("domain") or state.domain or "0000"

    # Handle --dry-run
    if dry_run:
        dry_payload = {
            "ok": True,
            "dry_run": True,
            "target_var": var_id,
            "target_th": th_id,
            "target_domain": target_domain,
            "format": export_format.lower(),
            "output_target": os.path.abspath(output_path) if output_path else "stdout",
            "estimated_requests": 1,
            "estimated_delay_seconds": 1.0,
            "status": "SAFE_TO_EXECUTE",
        }
        emit_output(dry_payload, as_json=ctx.obj.get("json", False))
        return

    # Real fetch
    raw_data = client.get_dynamic_data(var_id=var_id, th_id=th_id, domain=target_domain)
    decoded_rows = client.decode_dynamic_data(raw_data)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        if export_format.lower() == "csv":
            import csv
            if decoded_rows:
                fieldnames = list(decoded_rows[0].keys())
                with open(out, "w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(decoded_rows)
            else:
                out.write_text("", encoding="utf-8")
        else:
            with open(out, "w", encoding="utf-8") as f:
                json.dump(decoded_rows, f, indent=2, ensure_ascii=False)

        store.log_trajectory("fetch", f"bps fetch --var {var_id} --th {th_id} --format {export_format} --output {output_path}")

        result_payload = {
            "ok": True,
            "message": f"Successfully exported {len(decoded_rows)} rows to {output_path}",
            "output_path": str(out.resolve()),
            "rows_count": len(decoded_rows),
            "format": export_format.lower(),
        }
        emit_output(result_payload, as_json=ctx.obj.get("json", False))
    else:
        store.log_trajectory("fetch", f"bps fetch --var {var_id} --th {th_id}")
        emit_output(decoded_rows, as_json=ctx.obj.get("json", False))


def main():
    cli(prog_name="bps")


if __name__ == "__main__":
    main()
