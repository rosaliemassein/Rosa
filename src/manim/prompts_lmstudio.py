"""
Lean LLM prompts for LMStudio manim code generation.
Optimized for small context windows — concise but with enough structure
to produce compilable Manim Community Edition code.
"""

# System prompt: concise instructions + code skeleton + pitfall warnings
LMSTUDIO_SYSTEM = """You are a Manim animator. OUTPUT ONLY MANIM PYTHON CODE. No explanations, no markdown.

REQUIRED CODE STRUCTURE (always follow this exact skeleton):
```
from manim import *

class <SceneName>(Scene):
    def construct(self):
        # your code here
        self.play(...)
        self.wait()
```

RULES:
1. Exactly ONE Scene class inheriting from Scene.
2. `from manim import *` as the only import (plus math/numpy if needed).
3. self.play() takes Animation objects: Write(), FadeIn(), Create(), Transform(), NOT raw Mobjects.
4. MathTex uses RAW strings with double backslashes: MathTex(r"\\frac{a}{b}"), MathTex(r"\\int_0^1").
5. Do NOT use .animate inside Transform(). Use: Transform(a, b), not Transform(a, b.animate...).
6. NEVER output markdown fences (```), comments outside Python syntax, or prose.
7. Follow the active gate tier policy (A, B, B+, C, or 3D-LITE) and stay inside it.
8. Do NOT invent symbols/classes/functions. If unsure, fallback to Text/Circle/Line/Arrow/VGroup + Create/Write/FadeIn/FadeOut/Transform.

TIER-A SAFE API (preferred):
- Mobjects: Text, Dot, Circle, Square, Arrow, Line, VGroup
- Layout: arrange, next_to, to_edge, move_to, shift, scale
- Animations: Create, Write, FadeIn, FadeOut, Transform

STRICTLY AVOID IN TIER-A:
- MathTex, Tex
- Axes, NumberPlane, ThreeDAxes
- ThreeDScene and any 3D/camera methods
- Custom undefined helpers (e.g., LargeMove)

REPLACEMENT HINTS (when fixing compile issues):
- MathTex/Tex -> Text
- Rectangle/Polygon/RegularPolygon/Triangle/Star -> Circle or Square
- GrowArrow -> Create(Arrow(...))
- Indicate/Flash/LaggedStart/ReplacementTransform -> Transform or FadeIn/FadeOut
- ValueTracker/always_redraw -> simple fixed animation steps
- Any unknown color token -> BLUE/GREEN/RED/YELLOW/WHITE/BLACK
- VMobject/custom mobject internals -> VGroup + basic shapes
- Axes/NumberPlane (if disallowed in active tier) -> Line + Dot + Text approximation
- there_and_back/smooth/linear/rate_functions -> omit rate_func and use simple run_time
- If using loop indices (i, j, t), define them explicitly before use
- BarChart/complex chart helpers -> Axes + Rectangle bars + Text labels
- BLUE_A/BLUE_B/BLUE_C (or other *_A..*_E variants) -> BLUE (or RED/GREEN/YELLOW/WHITE/BLACK)

STYLE:
- Keep scenes simple and compilable first.
- Prefer 4-10 animation steps and readable text blocks."""

LMSTUDIO_TIER_A_ADDENDUM = """
ACTIVE GATE TIER: A (strict core subset)
- Prefer: Text, Dot, Circle, Square, Arrow, Line, VGroup
- Avoid: Tex/MathTex, Axes/NumberPlane, trackers, 3D/camera APIs
"""

LMSTUDIO_TIER_B_ADDENDUM = """
ACTIVE GATE TIER: B (expanded 2D subset)
- Allowed additions: Rectangle, Polygon, RegularPolygon, Triangle, Star, Tex/MathTex
- Allowed helpers: LaggedStart, ReplacementTransform, Succession, AnimationGroup, Indicate, Flash
- Keep disallowed: Axes, NumberPlane, ValueTracker/always_redraw, all 3D/camera APIs
- If uncertain, fallback to Tier-A core symbols.
- Do NOT use: VMobject, UpdateFromAlphaFunc, custom rate functions (`smooth`, `there_and_back`, `linear`) unless explicitly defined/imported.
- Do NOT emit undeclared identifiers; common failure is using `t` without definition.
- Prefer deterministic primitives: VGroup, Circle/Square/Line/Arrow, and Transform/FadeIn/FadeOut.
"""

LMSTUDIO_TIER_C_ADDENDUM = """
ACTIVE GATE TIER: C (advanced 2D subset)
- Allowed additions: Axes, NumberPlane, ValueTracker, always_redraw, DecimalNumber, DashedLine
- Keep disallowed: all 3D/camera APIs (ThreeDScene, ThreeDAxes, move_camera, set_camera_orientation)
- Prefer simple, stable axes usage and short updater chains.
"""

LMSTUDIO_TIER_BPLUS_ADDENDUM = """
ACTIVE GATE TIER: B+ (advanced 2D, no 3D)
- Allowed additions: Axes, NumberPlane, ValueTracker, always_redraw, DecimalNumber, DashedLine
- Keep disallowed: all 3D/camera APIs (ThreeDScene, ThreeDAxes, move_camera, set_camera_orientation)
- Prefer simple, stable axes usage and short updater chains.
- Avoid BarChart and uncommon color variants (BLUE_A/BLUE_C, etc.); use Axes + Rectangle and base colors.
"""

LMSTUDIO_TIER_3DLITE_ADDENDUM = """
ACTIVE GATE TIER: 3D-LITE (narrow 3D subset)
- Allowed additions: ThreeDScene, ThreeDAxes, set_camera_orientation
- Keep disallowed: move_camera, begin_ambient_camera_rotation, stop_ambient_camera_rotation, Surface
- Prefer one static 3D viewpoint and short, deterministic animations.
- For colors, stick to base constants (BLUE, RED, GREEN, YELLOW, WHITE, BLACK).
"""


LMSTUDIO_INPUT = """Generate Manim code for this concept animation.

Here is the full slide data in JSON format:
```json
{slide_json}
```

Use the 'voice' for narration, 'goal' for the objective, and 'remarks' for the detailed animation blueprint.
{formula_section}"""


LMSTUDIO_WITH_FORMULA = """
Also, use this formula as a reference:
{formula}
"""


# For fresh-retry: start a new conversation with avoidance notes
LMSTUDIO_RETRY_AVOIDANCE = """Generate Manim code for this concept animation.

Here is the full slide data in JSON format:
```json
{slide_json}
```
{formula_section}
IMPORTANT — AVOID THESE MISTAKES from a previous failed attempt:
{avoidance_notes}

COMPILE-FIRST RETRY POLICY:
- Prioritize valid, simple code over ambitious visuals.
- If a symbol is uncertain, replace it with a known symbol from the active tier.
- Ensure all names are defined before use.
- If error mentions disallowed or undefined symbol, replace with an active-tier alternative immediately.
- If error mentions `VMobject`, `Axes`, `ValueTracker`, `smooth`, `there_and_back`, `BarChart`, `BLUE_A`, `BLUE_C`, or undefined `t`, remove them and rewrite with basic Tier-safe primitives.
- Output ONLY Python code."""


LMSTUDIO_COMPILE_ERROR = """Your code FAILED to compile. Here is the full error log:
```
{error}
```

Fix the code. Output ONLY corrected Python code."""


LMSTUDIO_FEEDBACK = """Your code compiled but visual review FAILED:
{feedback}

Fix the issues. Keep animation dynamic. Output ONLY corrected Python code."""


# =============================================================================
# GPT-5-MINI TUTOR PROMPTS
# =============================================================================

MANIM_TUTOR_SYSTEM = """You are a Manim programming tutor. Your goal is to fix the student's code so it compiles and runs successfully.

CRITICAL:
1. You must preserve the ORIGINAL VIDEO IDEA from the student's prompt. Do NOT change the animation concept unless absolutely necessary to fix the error.
2. Output ONLY valid Python code. No explanations, no markdown fences.
3. Fix the specific compilation/runtime errors reported in the log.
4. Ensure the code is complete and self-contained (imports, Scene class, etc.).

REFERENCE EXAMPLES (Use these patterns):

# 1. Basic Animation & Transform
from manim import *
class MovingGroupToDestination(Scene):
    def construct(self):
        group = VGroup(Dot(LEFT), Dot(ORIGIN), Dot(RIGHT, color=RED), Dot(2 * RIGHT)).scale(1.4)
        dest = Dot([4, 3, 0], color=YELLOW)
        self.add(group, dest)
        self.play(group.animate.shift(dest.get_center() - group[2].get_center()))
        self.wait(0.5)

# 2. Moving Angle & Updaters
from manim import *
class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT
        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        
        line_moving.rotate(theta_tracker.get_value() * DEGREES, about_point=rotation_center)
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\\theta").move_to(
            Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        )
        
        self.add(line1, line_moving, a, tex)
        
        # Updaters for continuous animation
        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(theta_tracker.get_value() * DEGREES, about_point=rotation_center)
        )
        a.add_updater(lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False)))
        tex.add_updater(lambda x: x.move_to(
            Angle(line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False).point_from_proportion(0.5)
        ))
        
        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.wait()

# 3. Plotting & Graphs
from manim import *
class SinAndCosFunctionPlot(Scene):
    def construct(self):
        axes = Axes(x_range=[-10, 10.3, 1], y_range=[-1.5, 1.5, 1], x_length=10)
        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        cos_graph = axes.plot(lambda x: np.cos(x), color=RED)
        
        sin_label = axes.get_graph_label(sin_graph, "\\\\sin(x)", x_val=-10, direction=UP / 2)
        cos_label = axes.get_graph_label(cos_graph, label="\\\\cos(x)")
        
        plot = VGroup(axes, sin_graph, cos_graph)
        labels = VGroup(sin_label, cos_label)
        self.add(plot, labels)
"""

MANIM_TUTOR_FIRST_FIX = """The following Manim code failed to compile.

ORIGINAL PROMPT (The Idea):
{original_prompt}

CODE THAT FAILED:
```python
{failed_code}
```

FULL ERROR LOG:
```
{error_log}
```
{vertical_section}
Please rewrite the code to fix the errors while keeping the original animation idea. Output ONLY the fixed Python code."""

MANIM_TUTOR_SUBSEQUENT_FIX = """The corrected code still failed to compile.

NEW ERROR LOG:
```
{error_log}
```

Please fix the code again. Output ONLY the fixed Python code."""


# =============================================================================
# VERTICAL FORMAT ADDENDUM
# =============================================================================

VERTICAL_ADDENDUM_LMSTUDIO = """
VERTICAL VIDEO FORMAT (9:16 portrait):
- Runtime frame is already portrait: frame_width=9, frame_height=16.
- Safe zone: x ∈ [-4, 4], y ∈ [-7, 7].
- Build phone-native layouts; do NOT design a wide scene.
- Do NOT add any `if __name__ == "__main__"` config block.
- Labels should use font_size >= 36.
- Equations should use font_size >= 44.
- Titles should use font_size >= 48.
- Prefer explicit font_size over global `.scale(0.4)` style shrinking.
- Stack major elements vertically (top/middle/bottom beats), avoid wide horizontal rows.
- For Axes in vertical mode, use tall geometry (e.g. x_length=6, y_length=9).
"""

VERTICAL_ADDENDUM_TUTOR = """
CRITICAL — VERTICAL VIDEO FORMAT (9:16 portrait, like a phone screen):
- Runtime frame is already portrait: frame_width=9, frame_height=16.
- Safe zone: x ∈ [-4, 4], y ∈ [-7, 7].
- Keep ALL essential content inside this zone.
- Do NOT add any `if __name__ == "__main__"` config block.
- Use phone-readable text sizes: labels >= 36, equations >= 44, titles >= 48.
- Compose scenes vertically in beats; avoid wide horizontal layouts.
- Prefer explicit font_size sizing over global downscales.
- Axes should be tall in portrait mode (e.g. x_length=6, y_length=9).

Example vertical pattern:
    title = Text("Concept", font_size=50).to_edge(UP, buff=0.4)
    eq = MathTex(r"y=f(x)", font_size=46).next_to(title, DOWN, buff=0.35)
    ax = Axes(x_range=[0, 10, 2], y_range=[0, 10, 2], x_length=6, y_length=9, tips=False).to_edge(DOWN, buff=0.6)
    graph = ax.plot(lambda x: 0.12*(x-5)**2 + 2.0, x_range=[0, 10], color=BLUE)
    dot = Dot(ax.c2p(8.5, 0.12*(8.5-5)**2 + 2.0), color=YELLOW)
    t = ValueTracker(8.5)
    dot.add_updater(lambda m: m.move_to(ax.c2p(t.get_value(), 0.12*(t.get_value()-5)**2 + 2.0)))
    self.play(Write(title), Write(eq))
    self.play(Create(ax), Create(graph), FadeIn(dot))
    self.play(t.animate.set_value(5.0), run_time=2.5)
"""
