"""
Structured error handling utilities for BPS CLI.
Ensures deterministic machine-readable JSON on stderr and proper exit codes.
"""

from __future__ import annotations

import functools
import json
import sys
from typing import Any, Callable, Dict, Optional

import click

from .stream import ascii_safe


class BPSError(Exception):
    """Base exception for BPS API errors."""

    def __init__(self, message: str, code: str = "E_BPS_ERROR", hint: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.hint = hint

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"ok": False, "code": self.code, "error": self.message}
        if self.hint:
            data["hint"] = self.hint
        return data


class BPSAuthError(BPSError):
    """Raised when BPS API key is missing or invalid."""

    def __init__(self, message: str = "BPS API key missing or unauthorized", hint: Optional[str] = "Check BPS_API_KEY in .env or pass --key"):
        super().__init__(message, code="E_BPS_AUTH", hint=hint)


class BPSRateLimitError(BPSError):
    """Raised when BPS WAF or rate limit threshold is triggered."""

    def __init__(self, message: str = "Rate limit or Perimeter WAF block triggered", hint: Optional[str] = "Wait 3-5 seconds and retry with backoff"):
        super().__init__(message, code="E_BPS_RATE_LIMIT", hint=hint)


class BPSNotFoundError(BPSError):
    """Raised when requested data or variable is not found."""

    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message, code="E_BPS_NOT_FOUND", hint=hint)


def handle_error(func: Callable) -> Callable:
    """Decorator to catch exceptions and emit structured errors on stderr."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context(silent=True)
        is_json = bool(ctx and ctx.obj and ctx.obj.get("json")) if ctx else False

        try:
            return func(*args, **kwargs)
        except click.exceptions.Exit:
            raise
        except BPSError as exc:
            _emit_error(exc.to_dict(), is_json=is_json)
            raise click.exceptions.Exit(1)
        except Exception as exc:
            err_dict = {
                "ok": False,
                "code": "E_INTERNAL",
                "error": str(exc),
                "hint": "Check parameter format or run with --help",
            }
            _emit_error(err_dict, is_json=is_json)
            raise click.exceptions.Exit(1)

    return wrapper


def _emit_error(err_dict: Dict[str, Any], is_json: bool) -> None:
    """Write structured error payload to stderr."""
    if is_json:
        output = json.dumps(err_dict, indent=2)
    else:
        output = f"Error [{err_dict.get('code', 'FAIL')}]: {err_dict.get('error', 'Unknown')}"
        if err_dict.get("hint"):
            output += f"\nHint: {err_dict['hint']}"

    if not sys.stderr.isatty():
        output = ascii_safe(output)

    sys.stderr.write(output + "\n")
    sys.stderr.flush()
