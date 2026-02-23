import unittest
from pathlib import Path

from src.manim.evaluator import evaluate_code
from src.manim.models import ManimCode


VALID_CODE = """
from manim import *

class DemoScene(Scene):
    def construct(self):
        c = Circle()
        self.play(Create(c))
        self.wait()
"""


class FakeExecutor:
    def __init__(self, success=True, stderr="", timeout=False):
        self.success = success
        self.stderr = stderr
        self.timeout = timeout
        self.execute_called = False

    def save_code(self, manim_code, version=1, vertical=False):
        return Path(f"/tmp/{manim_code.slide_id}_v{version}.py")

    def execute(self, *args, **kwargs):
        self.execute_called = True
        if self.timeout:
            return False, None, "timeout: exceeded 90s"
        return self.success, None if not self.success else Path("/tmp/video.mp4"), self.stderr


class EvaluateCodeTests(unittest.TestCase):
    def test_gate_fail_skips_render(self):
        code = """from manim import *\nclass A(Scene):\n    pass"""
        executor = FakeExecutor()
        result = evaluate_code(
            manim_code=ManimCode(slide_id="s1", scene_name="A", code=code),
            executor=executor,
        )
        self.assertEqual(result.reward, -1)
        self.assertEqual(result.error_bucket, "gate_fail")
        self.assertFalse(executor.execute_called)

    def test_classifies_syntax_bucket(self):
        executor = FakeExecutor(success=False, stderr="SyntaxError: invalid syntax")
        result = evaluate_code(
            manim_code=ManimCode(slide_id="s1", scene_name="DemoScene", code=VALID_CODE),
            executor=executor,
        )
        self.assertEqual(result.reward, -1)
        self.assertEqual(result.error_bucket, "syntax")

    def test_classifies_undefined_name_bucket(self):
        executor = FakeExecutor(success=False, stderr="NameError: name 'foo' is not defined")
        result = evaluate_code(
            manim_code=ManimCode(slide_id="s1", scene_name="DemoScene", code=VALID_CODE),
            executor=executor,
        )
        self.assertEqual(result.reward, -1)
        self.assertEqual(result.error_bucket, "undefined_name")

    def test_classifies_timeout_bucket(self):
        executor = FakeExecutor(timeout=True)
        result = evaluate_code(
            manim_code=ManimCode(slide_id="s1", scene_name="DemoScene", code=VALID_CODE),
            executor=executor,
        )
        self.assertEqual(result.reward, -1)
        self.assertEqual(result.error_bucket, "timeout")

    def test_success_reward(self):
        executor = FakeExecutor(success=True)
        result = evaluate_code(
            manim_code=ManimCode(slide_id="s1", scene_name="DemoScene", code=VALID_CODE),
            executor=executor,
        )
        self.assertEqual(result.reward, 1)
        self.assertTrue(result.compiled)


if __name__ == "__main__":
    unittest.main()
