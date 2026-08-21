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


if __name__ == "__main__":
    unittest.main()
