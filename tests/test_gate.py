import unittest

from src.manim.gate import GateConfig, make_gate_config, validate_manim_code


VALID_CODE = """
from manim import *

class DemoScene(Scene):
    def construct(self):
        a = Circle()
        b = Square()
        self.play(Create(a), Transform(a, b))
        self.wait()
"""


class GateTests(unittest.TestCase):
    def test_valid_code_passes(self):
        result = validate_manim_code(VALID_CODE)
        self.assertTrue(result["gate_pass"])
        self.assertEqual(result["gate_errors"], [])

    def test_rejects_multi_scene(self):
        code = """
from manim import *
class A(Scene):
    def construct(self): pass
class B(Scene):
    def construct(self): pass
"""
        result = validate_manim_code(code)
        self.assertFalse(result["gate_pass"])
        self.assertTrue(any("exactly one class inheriting Scene" in e for e in result["gate_errors"]))

    def test_rejects_missing_construct(self):
        code = """
from manim import *
class A(Scene):
    def nope(self): pass
"""
        result = validate_manim_code(code)
        self.assertFalse(result["gate_pass"])
        self.assertTrue(any("missing construct()" in e for e in result["gate_errors"]))

    def test_flags_undefined_names(self):
        code = """
from manim import *
class A(Scene):
    def construct(self):
        self.play(Create(unknown_shape))
"""
        result = validate_manim_code(code)
        self.assertFalse(result["gate_pass"])
        self.assertIn("unknown_shape", result["undefined_names"])

    def test_detects_features(self):
        code = """
from manim import *
class A(ThreeDScene):
    def construct(self):
        ax = Axes()
        plane = NumberPlane()
        f = MathTex(r"x")
        self.add(ax, plane, f)
"""
        result = validate_manim_code(code, config=GateConfig(enforce_subset=False))
        self.assertIn("uses_mathtex", result["detected_features"])
        self.assertIn("uses_axes_or_numberplane", result["detected_features"])
        self.assertIn("uses_3d", result["detected_features"])

    def test_enforces_subset_toggles(self):
        code = """
from manim import *
class A(Scene):
    def construct(self):
        t = MathTex(r"x")
        self.play(Write(t))
"""
        strict = validate_manim_code(code, config=GateConfig(enforce_subset=True, allow_mathtex=False))
        permissive = validate_manim_code(code, config=GateConfig(enforce_subset=True, allow_mathtex=True))
        self.assertFalse(strict["gate_pass"])
        self.assertTrue(any("disallowed symbols/features" in e for e in strict["gate_errors"]))
        self.assertTrue(permissive["gate_pass"])

    def test_tiered_gate_configs(self):
        tier_b = make_gate_config("B")
        tier_bplus = make_gate_config("B+")
        tier_c = make_gate_config("C")
        tier_3d = make_gate_config("3D-LITE")
        self.assertIn("Rectangle", tier_b.allowed_symbols)
        self.assertNotIn("Axes", tier_b.allowed_symbols)
        self.assertIn("Axes", tier_bplus.allowed_symbols)
        self.assertIn("Axes", tier_c.allowed_symbols)
        self.assertIn("ThreeDAxes", tier_3d.allowed_symbols)
        self.assertFalse(tier_b.allow_3d)
        self.assertFalse(tier_bplus.allow_3d)
        self.assertFalse(tier_c.allow_3d)
        self.assertTrue(tier_3d.allow_3d)


if __name__ == "__main__":
    unittest.main()
