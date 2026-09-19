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
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


PROJECT_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = PROJECT_DIR / "app" / "static"
LOCAL_DIR = PROJECT_DIR / ".local"
LAB_CONFIG = PROJECT_DIR / ".lab.conf"
PROGRESS_FILE = LOCAL_DIR / "progress.json"
NOTES_FILE = LOCAL_DIR / "notes.json"
AI_SETTINGS_FILE = LOCAL_DIR / "ai-settings.json"
AI_SECRET_FILE = LOCAL_DIR / "ai-api-key"
ALLOWED_HOSTS = {"127.0.0.1", "localhost", "[::1]"}
MAX_BODY = 100_000
MAX_NOTE_LENGTH = 10_000
MAX_SPEECH_LENGTH = 1_000
SPEECH_SETUP_TIMEOUT = 600
AI_TIMEOUT = 45
AI_PROVIDERS = {"none", "ollama", "openai-compatible", "openai"}
DEFAULT_AI_SETTINGS = {
    "provider": "none",
    "baseUrl": "",
    "model": "",
    "sendLesson": True,
    "sendOutput": True,
    "sendNotes": True,
}

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


def load_ai_settings() -> dict:
    stored = load_json_file(AI_SETTINGS_FILE)
    settings = DEFAULT_AI_SETTINGS | {key: stored[key] for key in DEFAULT_AI_SETTINGS if key in stored}
    if settings["provider"] not in AI_PROVIDERS:
        return DEFAULT_AI_SETTINGS.copy()
    return settings


def public_ai_settings() -> dict:
    settings = load_ai_settings()
    settings["apiKeyConfigured"] = bool(os.environ.get("OPENAI_API_KEY") or AI_SECRET_FILE.is_file())
    return settings


def validate_ai_settings(payload: dict) -> dict:
    provider = payload.get("provider")
    base_url = payload.get("baseUrl", "").strip().rstrip("/")
    model = payload.get("model", "").strip()
    if provider not in AI_PROVIDERS:
        raise ValueError("Unsupported AI provider")
    if provider in {"ollama", "openai-compatible"}:
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("AI server must be a valid HTTP(S) URL without embedded credentials")
        if provider == "ollama" and parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("Ollama must use a local loopback address")
    if provider != "none" and not model:
        raise ValueError("An AI model is required")
    result = {"provider": provider, "baseUrl": base_url, "model": model}
    for key in ("sendLesson", "sendOutput", "sendNotes"):
        value = payload.get(key)
        if not isinstance(value, bool):
            raise ValueError("Invalid AI privacy setting")
        result[key] = value
    return result


def save_secret(value: str) -> None:
    LOCAL_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = AI_SECRET_FILE.with_suffix(".tmp")
    temporary.write_text(value)
    os.chmod(temporary, 0o600)
    temporary.replace(AI_SECRET_FILE)


def ai_api_key() -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    try:
        return AI_SECRET_FILE.read_text().strip()
    except OSError:
        return ""


def ai_request(url: str, payload: dict, api_key: str = "") -> dict:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request(url, data=json.dumps(payload).encode(), headers=headers, method="POST")
    try:
        with urlopen(request, timeout=AI_TIMEOUT) as response:
            result = json.loads(response.read())
    except HTTPError as exc:
        detail = exc.read(2_000).decode(errors="replace")
        raise RuntimeError(f"AI server returned HTTP {exc.code}: {detail}") from exc
    except (URLError, TimeoutError) as exc:
        raise RuntimeError(f"Could not reach AI server: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("AI server returned invalid JSON") from exc
    if not isinstance(result, dict):
        raise RuntimeError("AI server returned an unexpected response")
    return result


def extract_openai_response(result: dict) -> str:
    if isinstance(result.get("output_text"), str):
        return result["output_text"].strip()
    parts = []
    for item in result.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") == "output_text":
                parts.append(content.get("text", ""))
    return "\n".join(parts).strip()


def ask_ai(settings: dict, system_prompt: str, user_prompt: str) -> str:
    provider = settings["provider"]
    model = settings["model"]
    if provider == "ollama":
        result = ai_request(
            f'{settings["baseUrl"]}/api/chat',
            {"model": model, "stream": False, "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]},
        )
        answer = result.get("message", {}).get("content", "")
    elif provider == "openai-compatible":
        base = settings["baseUrl"]
        endpoint = f"{base}/chat/completions" if base.endswith("/v1") else f"{base}/v1/chat/completions"
        result = ai_request(
            endpoint,
            {"model": model, "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]},
            ai_api_key(),
        )
        choices = result.get("choices", [])
        answer = choices[0].get("message", {}).get("content", "") if choices else ""
    elif provider == "openai":
        key = ai_api_key()
        if not key:
            raise ValueError("OpenAI API key is not configured")
        result = ai_request(
            "https://api.openai.com/v1/responses",
            {"model": model, "instructions": system_prompt, "input": user_prompt, "store": False},
            key,
        )
        answer = extract_openai_response(result)
    else:
        raise ValueError("AI guidance is not configured")
    if not isinstance(answer, str) or not answer.strip():
        raise RuntimeError("AI server returned no feedback")
    return answer.strip()


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
                    "aiSettings": public_ai_settings(),
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
        language = load_lesson_language()
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
            if path == "/api/ai/settings":
                settings = validate_ai_settings(payload)
                api_key = payload.get("apiKey", "")
                if not isinstance(api_key, str) or len(api_key) > 500:
                    raise ValueError("Invalid API key")
                save_json_file(AI_SETTINGS_FILE, settings)
                if api_key.strip():
                    save_secret(api_key.strip())
                self._send_json(HTTPStatus.OK, public_ai_settings())
                return
            if path == "/api/ai/test":
                self._test_ai()
                return
            if path == "/api/ai/review":
                self._review_with_ai(payload, language)
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
        except RuntimeError as exc:
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": str(exc)})

    def _test_ai(self) -> None:
        settings = load_ai_settings()
        answer = ask_ai(settings, "Reply concisely.", "Reply with exactly: connection successful")
        self._send_json(HTTPStatus.OK, {"connected": True, "reply": answer[:500]})

    def _review_with_ai(self, payload: dict, language: str) -> None:
        lesson_id = payload.get("lessonId")
        note = payload.get("note", "")
        output = payload.get("output", "")
        if lesson_id not in LESSONS or not isinstance(note, str) or not isinstance(output, str):
            raise ValueError("Invalid AI review request")
        if len(note) > MAX_NOTE_LENGTH or len(output) > 50_000:
            raise ValueError("AI review input is too large")
        settings = load_ai_settings()
        language_name = "Dutch" if language == "nl" else "English"
        system_prompt = (
            f"You are a cybersecurity teacher. Reply in {language_name}. The learner only tests the explicitly "
            "permitted target. Distinguish observations, interpretations, and uncertainty. Praise correct reasoning, "
            "identify unsupported conclusions, give a small hint before any solution, and finish with one control question. "
            "Never propose testing another target and never execute commands."
        )
        sections = [f"Lesson: {LESSONS[lesson_id]['title'][language]}", f"Target: {LESSONS[lesson_id]['target']}"]
        if settings["sendLesson"]:
            sections.append("Lesson material:\n" + LESSONS[lesson_id]["files"][language].read_text()[:12_000])
        if settings["sendOutput"]:
            sections.append("Command output:\n" + output[:20_000])
        if settings["sendNotes"]:
            sections.append("Learner answer:\n" + note)
        sections.append("Give formative feedback, not a grade.")
        feedback = ask_ai(settings, system_prompt, "\n\n".join(sections))
        self._send_json(HTTPStatus.OK, {"feedback": feedback[:20_000]})

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
