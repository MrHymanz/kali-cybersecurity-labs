#!/usr/bin/env python3
"""Local, dependency-free web interface for Kali Cybersecurity Labs."""

from __future__ import annotations

import json
import os
import re
import subprocess
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


PROJECT_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = PROJECT_DIR / "app" / "static"
LOCAL_DIR = PROJECT_DIR / ".local"
LAB_CONFIG = PROJECT_DIR / ".lab.conf"
PROGRESS_FILE = LOCAL_DIR / "progress.json"
NOTES_FILE = LOCAL_DIR / "notes.json"
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "[::1]"}
MAX_BODY = 32_768
MAX_NOTE_LENGTH = 10_000
MAX_SPEECH_LENGTH = 1_000
SPEECH_SETUP_TIMEOUT = 600

LESSONS = {
    "web-enumeration-beginner": {
        "title": {
            "en": "Web enumeration fundamentals",
            "nl": "Basisprincipes van web-enumeration",
        },
        "summary": {
            "en": "Inspect a permitted web application carefully and separate observations from conclusions.",
            "nl": "Inspecteer een toegestane webapplicatie zorgvuldig en scheid observaties van conclusies.",
        },
        "files": {
            "en": PROJECT_DIR / "tutorials" / "en" / "web-enumeration-beginner.md",
            "nl": PROJECT_DIR / "tutorials" / "nl" / "web-enumeration-beginner.md",
        },
        "action": "fetch_headers",
        "target": "http://127.0.0.1:3000/",
    }
}

ACTIONS = {
    "fetch_headers": {
        "argv": [
            "curl",
            "--head",
            "--silent",
            "--show-error",
            "--max-time",
            "10",
            "http://127.0.0.1:3000/",
        ],
        "display": "curl -I http://127.0.0.1:3000/",
    }
}


def load_lesson_language() -> str:
    try:
        match = re.fullmatch(r"LESSON_LANGUAGE=(en|nl)\n?", LAB_CONFIG.read_text())
    except FileNotFoundError:
        return "en"
    return match.group(1) if match else "en"


def save_lesson_language(language: str) -> None:
    if language not in {"en", "nl"}:
        raise ValueError("Unsupported language")
    LAB_CONFIG.write_text(f"LESSON_LANGUAGE={language}\n")


def load_json_file(path: Path) -> dict:
    try:
        value = json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def save_json_file(path: Path, value: dict) -> None:
    LOCAL_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    os.chmod(temporary, 0o600)
    temporary.replace(path)


def public_lesson(lesson_id: str, language: str) -> dict:
    lesson = LESSONS[lesson_id]
    return {
        "id": lesson_id,
        "title": lesson["title"][language],
        "summary": lesson["summary"][language],
        "target": lesson["target"],
        "action": lesson["action"],
        "command": ACTIONS[lesson["action"]]["display"],
    }


class LabHandler(SimpleHTTPRequestHandler):
    server_version = "KaliLabsGUI/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format_string: str, *args) -> None:
        print(f"[{self.log_date_time_string()}] {format_string % args}")

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; style-src 'self'; script-src 'self'; "
            "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'",
        )
        super().end_headers()

    def _request_host_is_local(self) -> bool:
        host = self.headers.get("Host", "").split(":", 1)[0].lower()
        return host in ALLOWED_HOSTS

    def _origin_is_local(self) -> bool:
        origin = self.headers.get("Origin")
        if not origin:
            return True
        parsed = urlparse(origin)
        return (
            parsed.scheme == "http"
            and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
            and parsed.port == self.server.server_port
        )

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ValueError("Invalid content length") from exc
        if length < 1 or length > MAX_BODY:
            raise ValueError("Invalid request size")
        if self.headers.get_content_type() != "application/json":
            raise ValueError("Content-Type must be application/json")
        value = json.loads(self.rfile.read(length))
        if not isinstance(value, dict):
            raise ValueError("JSON object required")
        return value

    def _guard_request(self, require_origin: bool = False) -> bool:
        if not self._request_host_is_local() or (require_origin and not self._origin_is_local()):
            self._send_json(HTTPStatus.FORBIDDEN, {"error": "Local requests only"})
            return False
        return True

    def do_GET(self) -> None:
        if not self._guard_request():
            return
        path = urlparse(self.path).path
        language = load_lesson_language()
        if path == "/api/state":
            progress = load_json_file(PROGRESS_FILE)
            notes = load_json_file(NOTES_FILE)
            self._send_json(
                HTTPStatus.OK,
                {
                    "language": language,
                    "speechConfigured": (PROJECT_DIR / ".tts.conf").is_file(),
                    "lessons": [public_lesson(lesson_id, language) for lesson_id in LESSONS],
                    "progress": progress,
                    "notes": notes,
                },
            )
            return
        if path.startswith("/api/lessons/"):
            lesson_id = path.removeprefix("/api/lessons/")
            if lesson_id not in LESSONS:
                self._send_json(HTTPStatus.NOT_FOUND, {"error": "Lesson not found"})
                return
            lesson = public_lesson(lesson_id, language)
            lesson["markdown"] = LESSONS[lesson_id]["files"][language].read_text()
            self._send_json(HTTPStatus.OK, lesson)
            return
        super().do_GET()

    def do_POST(self) -> None:
        if not self._guard_request(require_origin=True):
            return
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
            if path == "/api/language":
                language = payload.get("language")
                save_lesson_language(language)
                self._send_json(HTTPStatus.OK, {"language": language})
                return
            if path == "/api/progress":
                lesson_id = payload.get("lessonId")
                complete = payload.get("complete")
                if lesson_id not in LESSONS or not isinstance(complete, bool):
                    raise ValueError("Invalid progress update")
                progress = load_json_file(PROGRESS_FILE)
                progress[lesson_id] = complete
                save_json_file(PROGRESS_FILE, progress)
                self._send_json(HTTPStatus.OK, {"saved": True})
                return
            if path == "/api/notes":
                lesson_id = payload.get("lessonId")
                note = payload.get("note")
                if lesson_id not in LESSONS or not isinstance(note, str) or len(note) > MAX_NOTE_LENGTH:
                    raise ValueError("Invalid note")
                notes = load_json_file(NOTES_FILE)
                notes[lesson_id] = note
                save_json_file(NOTES_FILE, notes)
                self._send_json(HTTPStatus.OK, {"saved": True})
                return
            if path == "/api/run":
                self._run_action(payload)
                return
            if path == "/api/speak":
                self._speak(payload)
                return
            if path == "/api/speech/configure":
                self._configure_speech(payload)
                return
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Endpoint not found"})
        except (ValueError, json.JSONDecodeError) as exc:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})

    def _run_action(self, payload: dict) -> None:
        lesson_id = payload.get("lessonId")
        action_id = payload.get("action")
        if lesson_id not in LESSONS or LESSONS[lesson_id]["action"] != action_id:
            raise ValueError("Action is not permitted for this lesson")
        action = ACTIONS[action_id]
        try:
            result = subprocess.run(
                action["argv"],
                cwd=PROJECT_DIR,
                capture_output=True,
                text=True,
                timeout=12,
                check=False,
                env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8"},
            )
            output = (result.stdout + result.stderr).strip()
            self._send_json(
                HTTPStatus.OK,
                {"command": action["display"], "exitCode": result.returncode, "output": output[:50_000]},
            )
        except FileNotFoundError:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "curl is not installed"})
        except subprocess.TimeoutExpired:
            self._send_json(HTTPStatus.GATEWAY_TIMEOUT, {"error": "The lab action timed out"})

    def _speak(self, payload: dict) -> None:
        text = payload.get("text")
        if not isinstance(text, str) or not text.strip() or len(text) > MAX_SPEECH_LENGTH:
            raise ValueError("Invalid speech text")
        if not (PROJECT_DIR / ".tts.conf").is_file():
            self._send_json(HTTPStatus.CONFLICT, {"error": "Speech is not configured"})
            return
        result = subprocess.run(
            [str(PROJECT_DIR / "scripts" / "speak.sh"), "--text", text],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if result.returncode:
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": result.stderr.strip() or "Speech failed"})
            return
        self._send_json(HTTPStatus.ACCEPTED, {"started": True})

    def _configure_speech(self, payload: dict) -> None:
        language = payload.get("language")
        if language not in {"en", "nl"}:
            raise ValueError("Unsupported speech language")
        try:
            result = subprocess.run(
                [str(PROJECT_DIR / "scripts" / "setup-speech.sh"), language],
                cwd=PROJECT_DIR,
                capture_output=True,
                text=True,
                timeout=SPEECH_SETUP_TIMEOUT,
                check=False,
            )
        except subprocess.TimeoutExpired:
            self._send_json(HTTPStatus.GATEWAY_TIMEOUT, {"error": "Speech setup timed out"})
            return
        if result.returncode:
            error = (result.stderr or result.stdout).strip()
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": error[-2_000:] or "Speech setup failed"},
            )
            return
        self._send_json(HTTPStatus.OK, {"configured": True})


def main() -> None:
    port_text = os.environ.get("KALI_LABS_PORT", "8080")
    if not port_text.isdigit() or not 1024 <= int(port_text) <= 65535:
        raise SystemExit("KALI_LABS_PORT must be a number from 1024 through 65535")
    server = ThreadingHTTPServer(("127.0.0.1", int(port_text)), LabHandler)
    print(f"Kali Cybersecurity Labs: http://127.0.0.1:{port_text}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
