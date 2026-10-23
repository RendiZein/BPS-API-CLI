"""
Stream handling and encoding resilience utilities.
Prevents Windows 'charmap' / cp1252 errors and prompt-toolkit piped terminal issues.
"""

from __future__ import annotations

import json
import sys
from typing import Any


def ascii_safe(value: Any) -> str:
    """Render text as reversible ASCII escapes for legacy or piped Windows output streams."""
    return str(value).encode("ascii", errors="backslashreplace").decode("ascii")


def supports_interactive_prompt(stdin=None, stdout=None) -> bool:
    """
    Return whether prompt_toolkit can safely attach to the current terminal.

    Redirected streams are common in CI, Click's CliRunner, and automated agent pipelines.
    On Windows prompt_toolkit raises NoConsoleScreenBufferError for redirected streams,
    so we keep rich prompts for real interactive terminals only.
    """
    stdin = sys.stdin if stdin is None else stdin
    stdout = sys.stdout if stdout is None else stdout
    try:
        return bool(stdin.isatty() and stdout.isatty())
    except (AttributeError, OSError):
        return False


def emit_output(data: Any, as_json: bool = False, ascii_fallback: bool = False) -> None:
    """
    Standard output dispatcher:
    - If as_json is True: writes cleanly formatted JSON to stdout.
    - If data is dict/list: formats readable text.
    - Applies ascii_safe when piped or in non-tty streams.
    """
    if as_json:
        serialized = json.dumps(data, indent=2, ensure_ascii=not ascii_fallback, default=str)
        if ascii_fallback:
            serialized = ascii_safe(serialized)
        sys.stdout.write(serialized + "\n")
        sys.stdout.flush()
    elif isinstance(data, dict):
        for k, v in data.items():
            line = f"{k}: {v}"
            if ascii_fallback or not sys.stdout.isatty():
                line = ascii_safe(line)
            sys.stdout.write(line + "\n")
        sys.stdout.flush()
    else:
        text = str(data)
        if ascii_fallback or not sys.stdout.isatty():
            text = ascii_safe(text)
        sys.stdout.write(text + "\n")
        sys.stdout.flush()
