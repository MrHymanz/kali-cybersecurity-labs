import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "app" / "server.py"
SPEC = importlib.util.spec_from_file_location("lab_server", MODULE_PATH)
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class ServerHelpersTest(unittest.TestCase):
    def test_manual_ai_discussion_controls_are_present(self):
        html = (MODULE_PATH.parent / "static" / "index.html").read_text()
        javascript = (MODULE_PATH.parent / "static" / "app.js").read_text()
        self.assertIn('id="copyDiscussionButton"', html)
        self.assertIn('data-i18n="manualChoiceTitle"', html)
        self.assertIn("function discussionText()", javascript)
        self.assertIn("navigator.clipboard.writeText", javascript)

    def test_public_lesson_exposes_only_expected_fields(self):
        lesson = server.public_lesson("web-enumeration-beginner", "en")
        self.assertEqual(lesson["target"], "http://127.0.0.1:3000/")
        self.assertEqual(lesson["command"], "curl -I http://127.0.0.1:3000/")
        self.assertNotIn("files", lesson)

    def test_action_is_fixed_and_loopback_only(self):
        action = server.ACTIONS["fetch_headers"]
        self.assertEqual(action["argv"][-1], "http://127.0.0.1:3000/")
        self.assertNotIn("shell", action)

    def test_json_state_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            with patch.object(server, "LOCAL_DIR", Path(directory)):
                server.save_json_file(path, {"lesson": True})
            self.assertEqual(server.load_json_file(path), {"lesson": True})
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_invalid_json_state_returns_empty_object(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text("not json")
            self.assertEqual(server.load_json_file(path), {})

    def test_language_defaults_to_english(self):
        with patch.object(server, "LAB_CONFIG", Path("/definitely/missing/.lab.conf")):
            self.assertEqual(server.load_lesson_language(), "en")

    def test_language_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ".lab.conf"
            with patch.object(server, "LAB_CONFIG", path):
                server.save_lesson_language("nl")
                self.assertEqual(server.load_lesson_language(), "nl")
                with self.assertRaises(ValueError):
                    server.save_lesson_language("de")

    def test_ai_settings_validate_local_backend(self):
        settings = server.validate_ai_settings({
            "provider": "ollama",
            "baseUrl": "http://127.0.0.1:11434/",
            "model": "llama3.2",
            "sendLesson": True,
            "sendOutput": True,
            "sendNotes": False,
        })
        self.assertEqual(settings["baseUrl"], "http://127.0.0.1:11434")
        self.assertFalse(settings["sendNotes"])

    def test_ai_settings_reject_embedded_credentials(self):
        with self.assertRaises(ValueError):
            server.validate_ai_settings({
                "provider": "openai-compatible",
                "baseUrl": "http://user:secret@127.0.0.1:8000",
                "model": "model",
                "sendLesson": True,
                "sendOutput": True,
                "sendNotes": True,
            })

    def test_ollama_is_restricted_to_loopback(self):
        with self.assertRaises(ValueError):
            server.validate_ai_settings({
                "provider": "ollama",
                "baseUrl": "http://192.168.1.20:11434",
                "model": "model",
                "sendLesson": True,
                "sendOutput": True,
                "sendNotes": True,
            })

    def test_ai_secret_is_private(self):
        with tempfile.TemporaryDirectory() as directory:
            secret = Path(directory) / "ai-api-key"
            with patch.object(server, "LOCAL_DIR", Path(directory)), patch.object(server, "AI_SECRET_FILE", secret):
                server.save_secret("test-secret")
            self.assertEqual(secret.read_text(), "test-secret")
            self.assertEqual(secret.stat().st_mode & 0o777, 0o600)

    def test_extract_openai_response(self):
        result = {"output": [{"content": [{"type": "output_text", "text": "Useful feedback"}]}]}
        self.assertEqual(server.extract_openai_response(result), "Useful feedback")

    def test_ollama_adapter_uses_local_chat_endpoint(self):
        settings = {"provider": "ollama", "baseUrl": "http://127.0.0.1:11434", "model": "test"}
        with patch.object(server, "ai_request", return_value={"message": {"content": "feedback"}}) as request:
            self.assertEqual(server.ask_ai(settings, "system", "user"), "feedback")
        self.assertEqual(request.call_args.args[0], "http://127.0.0.1:11434/api/chat")

    def test_openai_requests_disable_storage(self):
        settings = {"provider": "openai", "baseUrl": "", "model": "test"}
        response = {"output": [{"content": [{"type": "output_text", "text": "feedback"}]}]}
        with patch.object(server, "ai_api_key", return_value="secret"), patch.object(server, "ai_request", return_value=response) as request:
            self.assertEqual(server.ask_ai(settings, "system", "user"), "feedback")
        self.assertFalse(request.call_args.args[1]["store"])


if __name__ == "__main__":
    unittest.main()
