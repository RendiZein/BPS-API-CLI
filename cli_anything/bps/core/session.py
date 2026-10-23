"""
Stateful session management and permanent trajectory logging for BPS CLI.
Features cross-platform atomic file locking (Windows msvcrt + POSIX fcntl) and a 50-level snapshot stack.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_SESSION_FILE = Path(".bps_session.json")
DEFAULT_TRAJECTORY_FILE = Path("trajectory.json")
MAX_SNAPSHOT_HISTORY = 50


@dataclass
class SessionState:
    domain: str = "0000"
    domain_name: str = "Nasional"
    subject_id: Optional[int] = None
    subject_name: Optional[str] = None
    var_id: Optional[int] = None
    var_name: Optional[str] = None
    session_name: str = "default"
    history: List[Dict[str, Any]] = field(default_factory=list)
    future: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "domain_name": self.domain_name,
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "var_id": self.var_id,
            "var_name": self.var_name,
            "session_name": self.session_name,
            "history": self.history[-MAX_SNAPSHOT_HISTORY:],
            "future": self.future[-MAX_SNAPSHOT_HISTORY:],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SessionState:
        return cls(
            domain=str(data.get("domain") or "0000"),
            domain_name=str(data.get("domain_name") or "Nasional"),
            subject_id=data.get("subject_id"),
            subject_name=data.get("subject_name"),
            var_id=data.get("var_id"),
            var_name=data.get("var_name"),
            session_name=str(data.get("session_name") or "default"),
            history=list(data.get("history") or []),
            future=list(data.get("future") or []),
        )


def _locked_save_json(path: Path, data: Any, **dump_kwargs: Any) -> None:
    """Save JSON safely with cross-platform atomic file locking (msvcrt on Windows, fcntl on POSIX)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = path.open("r+", encoding="utf-8")
    except FileNotFoundError:
        handle = path.open("w+", encoding="utf-8")

    with handle:
        locked = False
        try:
            import fcntl
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            locked = True
        except (ImportError, OSError):
            try:
                import msvcrt
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
                locked = True
            except (ImportError, OSError):
                pass

        try:
            handle.seek(0)
            handle.truncate()
            json.dump(data, handle, **dump_kwargs)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        finally:
            if locked:
                try:
                    import fcntl
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
                except (ImportError, OSError):
                    try:
                        import msvcrt
                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                    except (ImportError, OSError):
                        pass


class SessionStore:
    def __init__(self, session_path: Optional[str | Path] = None, trajectory_path: Optional[str | Path] = None):
        self.session_path = Path(session_path) if session_path else DEFAULT_SESSION_FILE
        self.trajectory_path = Path(trajectory_path) if trajectory_path else DEFAULT_TRAJECTORY_FILE

    def load(self) -> SessionState:
        if not self.session_path.exists():
            return SessionState()
        try:
            with open(self.session_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                return SessionState()
            return SessionState.from_dict(data)
        except (json.JSONDecodeError, OSError):
            return SessionState()

    def save(self, state: SessionState) -> Path:
        _locked_save_json(self.session_path, state.to_dict(), indent=2, sort_keys=True)
        return self.session_path

    def record_snapshot(self, state: SessionState, action: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Capture current state before mutation so it can be undone."""
        snapshot = {
            "action": action,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domain": state.domain,
            "domain_name": state.domain_name,
            "subject_id": state.subject_id,
            "var_id": state.var_id,
            "details": details or {},
        }
        state.history.append(snapshot)
        if len(state.history) > MAX_SNAPSHOT_HISTORY:
            state.history.pop(0)
        state.future.clear()
        self.save(state)

    def undo(self, state: SessionState) -> Dict[str, Any]:
        """Roll back to the previous state snapshot."""
        if not state.history:
            raise ValueError("No session history to undo.")

        current_snapshot = {
            "domain": state.domain,
            "domain_name": state.domain_name,
            "subject_id": state.subject_id,
            "var_id": state.var_id,
        }
        state.future.append(current_snapshot)

        last_snapshot = state.history.pop()
        state.domain = last_snapshot.get("domain", "0000")
        state.domain_name = last_snapshot.get("domain_name", "Nasional")
        state.subject_id = last_snapshot.get("subject_id")
        state.var_id = last_snapshot.get("var_id")
        self.save(state)
        return last_snapshot

    def redo(self, state: SessionState) -> Dict[str, Any]:
        """Re-apply a previously undone state snapshot."""
        if not state.future:
            raise ValueError("No session actions to redo.")

        current_snapshot = {
            "domain": state.domain,
            "domain_name": state.domain_name,
            "subject_id": state.subject_id,
            "var_id": state.var_id,
        }
        state.history.append(current_snapshot)

        next_snapshot = state.future.pop()
        state.domain = next_snapshot.get("domain", "0000")
        state.domain_name = next_snapshot.get("domain_name", "Nasional")
        state.subject_id = next_snapshot.get("subject_id")
        state.var_id = next_snapshot.get("var_id")
        self.save(state)
        return next_snapshot

    def log_trajectory(
        self,
        step_id: str,
        command: str,
        status: str = "success",
        bundle_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Append a durable replay event to trajectory.json."""
        record = {
            "step_id": step_id,
            "command": command,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": status,
            "bundle_id": bundle_id,
            "notes": notes,
        }
        records = []
        if self.trajectory_path.exists():
            try:
                with open(self.trajectory_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
                if not isinstance(records, list):
                    records = []
            except (json.JSONDecodeError, OSError):
                records = []

        records.append(record)
        _locked_save_json(self.trajectory_path, records, indent=2)
