"""
Compile-first validity gate for generated Manim code.
"""

from __future__ import annotations

import ast
import builtins
from dataclasses import dataclass, field
from typing import Any


FeatureName = str

TIER_A_ALLOWED_SYMBOLS = {
    # Core shapes/text and layout
    "Text",
    "Dot",
    "Circle",
    "Square",
    "Arrow",
    "Line",
    "VGroup",
    "Group",
    "arrange",
    "next_to",
    "to_edge",
    "move_to",
    "shift",
    "scale",
    # Core animations
    "Create",
    "Write",
    "FadeIn",
    "FadeOut",
    "Transform",
    # Skeleton/runtime symbols
    "Scene",
    "ThreeDScene",
    "self",
    # Common coordinates/constants/colors
    "UP",
    "DOWN",
    "LEFT",
    "RIGHT",
    "UL",
    "UR",
    "DL",
    "DR",
    "ORIGIN",
    "PI",
    "TAU",
    "DEGREES",
    "RED",
    "BLUE",
    "GREEN",
    "YELLOW",
    "PURPLE",
    "ORANGE",
    "GOLD",
    "WHITE",
    "BLACK",
    "GRAY",
    "GREY",
}

TIER_B_ADDITIONAL_SYMBOLS = {
    # Commonly requested 2D geometry/text upgrades
    "Rectangle",
    "RoundedRectangle",
    "Polygon",
    "RegularPolygon",
    "Triangle",
    "Star",
    "Tex",
    "MathTex",
    "ImageMobject",
    "SurroundingRectangle",
    # Compile-safe animation helpers
    "LaggedStart",
    "ReplacementTransform",
    "Succession",
    "AnimationGroup",
    "Indicate",
    "Flash",
    "GrowArrow",
    # Additional colors frequently used by model outputs
    "GRAY_A",
    "GRAY_B",
    "GRAY_C",
    "GRAY_D",
    "GRAY_E",
    "GREY_A",
    "GREY_B",
    "GREY_C",
    "GREY_D",
    "GREY_E",
}

TIER_C_ADDITIONAL_SYMBOLS = {
    # Advanced but still 2D-focused tools
    "Axes",
    "NumberPlane",
    "ValueTracker",
    "always_redraw",
    "DecimalNumber",
    "DashedLine",
}

TIER_3DLITE_ADDITIONAL_SYMBOLS = {
    # Narrow 3D subset (basic scene + axes + camera orientation only)
    "ThreeDScene",
    "ThreeDAxes",
    "set_camera_orientation",
}

TIER_A_DISALLOWED_SYMBOLS = {
    "MathTex",
    "ThreeDScene",
    "ThreeDAxes",
    "Tex",
    "Surface",
    "Rectangle",
    "Polygon",
    "RegularPolygon",
    "Triangle",
    "Star",
    "Axes",
    "NumberPlane",
    "ValueTracker",
    "always_redraw",
    "move_camera",
    "set_camera_orientation",
    "begin_ambient_camera_rotation",
    "stop_ambient_camera_rotation",
}

TIER_B_DISALLOWED_SYMBOLS = {
    # Tier B keeps 3D/camera and advanced plot helpers disabled.
    "ThreeDScene",
    "ThreeDAxes",
    "Surface",
    "Axes",
    "NumberPlane",
    "ValueTracker",
    "always_redraw",
    "move_camera",
    "set_camera_orientation",
    "begin_ambient_camera_rotation",
    "stop_ambient_camera_rotation",
}

TIER_C_DISALLOWED_SYMBOLS = {
    # Tier C still blocks 3D/camera-heavy APIs.
    "ThreeDScene",
    "ThreeDAxes",
    "Surface",
    "move_camera",
    "set_camera_orientation",
    "begin_ambient_camera_rotation",
    "stop_ambient_camera_rotation",
}

TIER_3DLITE_DISALLOWED_SYMBOLS = {
    # 3D-lite keeps advanced camera/3D helpers disabled.
    "Surface",
    "move_camera",
    "begin_ambient_camera_rotation",
    "stop_ambient_camera_rotation",
}


@dataclass
class GateConfig:
    """Configuration for Phase 1 compile-first gating."""

    enforce_subset: bool = True
    allow_mathtex: bool = False
    allow_3d: bool = False
    allowed_symbols: set[str] = field(
        default_factory=lambda: set(TIER_A_ALLOWED_SYMBOLS)
    )
    disallowed_symbols: set[str] = field(
        default_factory=lambda: set(TIER_A_DISALLOWED_SYMBOLS)
    )


MANIM_SYMBOLS_REQUIRING_ALLOWLIST = {
    "Text",
    "Dot",
    "Circle",
    "Square",
    "Arrow",
    "Line",
    "VGroup",
    "Create",
    "Write",
    "FadeIn",
    "FadeOut",
    "Transform",
    "MathTex",
    "Tex",
    "Axes",
    "NumberPlane",
    "ThreeDAxes",
    "ThreeDScene",
    "ValueTracker",
    "Rectangle",
    "Polygon",
    "RegularPolygon",
    "RoundedRectangle",
    "Triangle",
    "Star",
    "Brace",
    "ImageMobject",
    "SurroundingRectangle",
    "LaggedStart",
    "ReplacementTransform",
    "Succession",
    "AnimationGroup",
    "Indicate",
    "Flash",
    "GrowArrow",
    "Table",
    "DashedLine",
}

FEATURE_TOKENS = {
    "uses_mathtex": {"MathTex"},
    "uses_axes_or_numberplane": {"Axes", "NumberPlane"},
    "uses_3d": {
        "ThreeDScene",
        "ThreeDAxes",
        "move_camera",
        "set_camera_orientation",
        "begin_ambient_camera_rotation",
        "stop_ambient_camera_rotation",
    },
}

def make_gate_config(tier: str = "A") -> GateConfig:
    normalized = (tier or "A").strip().upper()
    if normalized in {"3DLITE", "3D-LITE"}:
        allowed = (
            set(TIER_A_ALLOWED_SYMBOLS)
            | set(TIER_B_ADDITIONAL_SYMBOLS)
            | set(TIER_C_ADDITIONAL_SYMBOLS)
            | set(TIER_3DLITE_ADDITIONAL_SYMBOLS)
        )
        return GateConfig(
            enforce_subset=True,
            allow_mathtex=True,
            allow_3d=True,
            allowed_symbols=allowed,
            disallowed_symbols=set(TIER_3DLITE_DISALLOWED_SYMBOLS),
        )
    if normalized in {"B+", "BPLUS"}:
        allowed = set(TIER_A_ALLOWED_SYMBOLS) | set(TIER_B_ADDITIONAL_SYMBOLS) | set(TIER_C_ADDITIONAL_SYMBOLS)
        return GateConfig(
            enforce_subset=True,
            allow_mathtex=True,
            allow_3d=False,
            allowed_symbols=allowed,
            disallowed_symbols=set(TIER_C_DISALLOWED_SYMBOLS),
        )
    if normalized == "C":
        allowed = set(TIER_A_ALLOWED_SYMBOLS) | set(TIER_B_ADDITIONAL_SYMBOLS) | set(TIER_C_ADDITIONAL_SYMBOLS)
        return GateConfig(
            enforce_subset=True,
            allow_mathtex=True,
            allow_3d=False,
            allowed_symbols=allowed,
            disallowed_symbols=set(TIER_C_DISALLOWED_SYMBOLS),
        )
    if normalized == "B":
        allowed = set(TIER_A_ALLOWED_SYMBOLS) | set(TIER_B_ADDITIONAL_SYMBOLS)
        return GateConfig(
            enforce_subset=True,
            allow_mathtex=True,
            allow_3d=False,
            allowed_symbols=allowed,
            disallowed_symbols=set(TIER_B_DISALLOWED_SYMBOLS),
        )
    return GateConfig(
        enforce_subset=True,
        allow_mathtex=False,
        allow_3d=False,
        allowed_symbols=set(TIER_A_ALLOWED_SYMBOLS),
        disallowed_symbols=set(TIER_A_DISALLOWED_SYMBOLS),
    )


def strip_markdown_fences(code: str) -> str:
    """Remove markdown code fences from generated code."""
    cleaned_lines: list[str] = []
    for line in code.splitlines():
        if line.strip().startswith("```"):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


class _NameCollector(ast.NodeVisitor):
    """Collect defined and referenced names for undefined-name checks."""

    def __init__(self) -> None:
        self.defined: set[str] = set()
        self.used: set[str] = set()
        self.called: set[str] = set()
        self.attr_used: set[str] = set()
        self.class_defs: list[ast.ClassDef] = []

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.defined.add(alias.asname or alias.name.split(".")[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        for alias in node.names:
            if alias.name == "*":
                # from manim import * handled by allowlist symbols
                continue
            self.defined.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.defined.add(node.name)
        self.class_defs.append(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.defined.add(node.name)
        for arg in node.args.posonlyargs + node.args.args + node.args.kwonlyargs:
            self.defined.add(arg.arg)
        if node.args.vararg:
            self.defined.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.defined.add(node.args.kwarg.arg)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.visit_FunctionDef(node)

    def visit_Name(self, node: ast.Name) -> Any:
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> Any:
        self._define_target(node.target)
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> Any:
        self.visit_For(node)

    def visit_With(self, node: ast.With) -> Any:
        for item in node.items:
            if item.optional_vars is not None:
                self._define_target(item.optional_vars)
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> Any:
        self.visit_With(node)

    def visit_comprehension(self, node: ast.comprehension) -> Any:
        self._define_target(node.target)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        if isinstance(node.func, ast.Name):
            self.called.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.attr_used.add(node.func.attr)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        self.attr_used.add(node.attr)
        self.generic_visit(node)

    def _define_target(self, target: ast.AST) -> None:
        if isinstance(target, ast.Name):
            self.defined.add(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                self._define_target(elt)


def _extract_scene_classes(tree: ast.Module) -> list[ast.ClassDef]:
    scene_classes: list[ast.ClassDef] = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id in {"Scene", "ThreeDScene"}:
                scene_classes.append(node)
            elif isinstance(base, ast.Attribute) and base.attr in {"Scene", "ThreeDScene"}:
                scene_classes.append(node)
    return scene_classes


def _has_construct_method(scene_cls: ast.ClassDef) -> bool:
    for node in scene_cls.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "construct":
            return True
    return False


def validate_manim_code(code: str, config: GateConfig | None = None) -> dict[str, Any]:
    """
    Validate generated Manim code for compile-first stabilization.

    Returns:
        {
            gate_pass: bool,
            gate_errors: list[str],
            detected_features: list[str],
            undefined_names: list[str]
        }
    """
    cfg = config or GateConfig()
    gate_errors: list[str] = []
    gate_reason_tags: set[str] = set()
    detected_features: set[FeatureName] = set()

    cleaned_code = strip_markdown_fences(code)

    if "from manim import *" not in cleaned_code:
        gate_errors.append("missing required import: from manim import *")
        gate_reason_tags.add("skeleton_missing_import")

    if "```" in cleaned_code:
        gate_errors.append("markdown fence residue detected")
        gate_reason_tags.add("format_markdown_fence")

    # Syntax checks (AST + compile equivalent).
    tree: ast.Module | None = None
    try:
        tree = ast.parse(cleaned_code)
        compile(cleaned_code, "<manim_generated>", "exec")
    except SyntaxError as exc:
        gate_errors.append(f"syntax error: {exc.msg} (line {exc.lineno})")
        gate_reason_tags.add("syntax_error")

    undefined_names: list[str] = []
    if tree is not None:
        scene_classes = _extract_scene_classes(tree)
        if len(scene_classes) != 1:
            gate_errors.append("expected exactly one class inheriting Scene or ThreeDScene")
            gate_reason_tags.add("skeleton_scene_count")
        elif not _has_construct_method(scene_classes[0]):
            gate_errors.append("scene class is missing construct()")
            gate_reason_tags.add("skeleton_missing_construct")

        collector = _NameCollector()
        collector.visit(tree)

        tokens_seen = collector.used | collector.called | collector.attr_used

        for feature_name, feature_tokens in FEATURE_TOKENS.items():
            if tokens_seen.intersection(feature_tokens):
                detected_features.add(feature_name)

        builtin_names = set(dir(builtins))
        always_known = set(cfg.allowed_symbols)
        if cfg.allow_mathtex:
            always_known.add("MathTex")
        if cfg.allow_3d:
            always_known.update({"ThreeDScene", "ThreeDAxes"})
        always_known |= builtin_names

        undefined = sorted(name for name in collector.used if name not in collector.defined and name not in always_known)
        undefined_names = undefined
        if undefined:
            gate_errors.append(f"undefined identifiers detected: {', '.join(undefined)}")
            gate_reason_tags.add("undefined_symbol")

        if cfg.enforce_subset:
            disallowed = set()
            effective_disallowed = set(cfg.disallowed_symbols)
            if cfg.allow_mathtex:
                effective_disallowed.discard("MathTex")
            if cfg.allow_3d:
                effective_disallowed.discard("ThreeDScene")
                effective_disallowed.discard("ThreeDAxes")
                effective_disallowed.discard("move_camera")
                effective_disallowed.discard("set_camera_orientation")
                effective_disallowed.discard("begin_ambient_camera_rotation")
                effective_disallowed.discard("stop_ambient_camera_rotation")

            for name in tokens_seen:
                if name in effective_disallowed:
                    disallowed.add(name)

            # Hard constrain to simple subset for known manim symbols.
            for name in tokens_seen:
                if (
                    name in MANIM_SYMBOLS_REQUIRING_ALLOWLIST
                    and name not in cfg.allowed_symbols
                ):
                    if cfg.allow_mathtex and name == "MathTex":
                        continue
                    if cfg.allow_3d and name in {"ThreeDScene", "ThreeDAxes"}:
                        continue
                    disallowed.add(name)

            if not cfg.allow_mathtex and "uses_mathtex" in detected_features:
                disallowed.add("MathTex")
            if not cfg.allow_3d and "uses_3d" in detected_features:
                disallowed.add("3d_features")

            if disallowed:
                gate_errors.append(
                    "disallowed symbols/features in constrained subset: "
                    + ", ".join(sorted(disallowed))
                )
                gate_reason_tags.add("disallowed_tier_symbol")

    return {
        "gate_pass": len(gate_errors) == 0,
        "gate_errors": gate_errors,
        "gate_reason_tags": sorted(gate_reason_tags),
        "detected_features": sorted(detected_features),
        "undefined_names": undefined_names,
    }
