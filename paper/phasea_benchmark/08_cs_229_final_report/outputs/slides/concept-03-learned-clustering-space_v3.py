from manim import *
import numpy as np

class LearnedClusteringSpace(Scene):
    def construct(self):
        # 1. Setup centers for split-screen view
        left_origin = LEFT * 3.5
        right_origin = RIGHT * 3.5
        
        # 2. Draw coordinate indicators using Lines (as Axes/NumberPlane are disallowed)
        l_horiz = Line(left_origin + LEFT * 2, left_origin + RIGHT * 2, color=WHITE)
        l_vert = Line(left_origin + DOWN * 2, left_origin + UP * 2, color=WHITE)
        r_horiz = Line(right_origin + LEFT * 2, right_origin + RIGHT * 2, color=WHITE)
        r_vert = Line(right_origin + DOWN * 2, right_origin + UP * 2, color=WHITE)
        
        dividing_line = Line(UP * 4, DOWN * 4, color=WHITE, stroke_width=1)
        axes_group = VGroup(l_horiz, l_vert, r_horiz, r_vert, dividing_line)
        
        # 3. Titles using Text (as MathTex/Tex might be disallowed)
        phys_text = Text("Physical Space", font_size=24).move_to(left_origin + UP * 2.5)
        learn_text = Text("Learned Space", font_size=24).move_to(right_origin + UP * 2.5)
        
        # 4. Generate dot clusters for Physical Space (Overlapping)
        np.random.seed(42)
        red_dots = VGroup()
        blue_dots = VGroup()
        
        for _ in range(30):
            # Create overlapping distributions near the left center
            r_offset = [np.random.normal(0.3, 0.5), np.random.normal(0.3, 0.5), 0]
            b_offset = [np.random.normal(-0.3, 0.5), np.random.normal(-0.3, 0.5), 0]
            
            red_dots.add(Dot(left_origin + r_offset, color=RED, radius=0.06))
            blue_dots.add(Dot(left_origin + b_offset, color=BLUE, radius=0.06))
            
        # 5. Define target positions for Learned Space (Separated)
        red_targets = VGroup()
        blue_targets = VGroup()
        
        for _ in range(30):
            # Red dots cluster on the left of the right pane
            rt_offset = [np.random.normal(-1.2, 0.3), np.random.normal(0, 0.3), 0]
            # Blue dots cluster on the right of the right pane
            bt_offset = [np.random.normal(1.2, 0.3), np.random.normal(0, 0.3), 0]
            
            red_targets.add(Dot(right_origin + rt_offset, color=RED, radius=0.06))
            blue_targets.add(Dot(right_origin + bt_offset, color=BLUE, radius=0.06))
            
        # 6. Classification indicator circles
        circle_red = Circle(radius=0.9, color=RED).move_to(right_origin + LEFT * 1.2)
        circle_blue = Circle(radius=0.9, color=BLUE).move_to(right_origin + RIGHT * 1.2)
        
        # 7. Simplified formula using Text
        formula = Text("L_V = 1/N * sum(q_j) * [sum(V_k components)]", font_size=18).to_edge(DOWN)
        
        # --- ANIMATION ---
        
        # Initial display
        self.add(axes_group, phys_text, learn_text)
        self.play(FadeIn(red_dots), FadeIn(blue_dots))
        self.wait(1)
        
        # Coordinate space transformation
        # Using Transform instead of ReplacementTransform (which was undefined)
        self.play(
            Transform(red_dots, red_targets),
            Transform(blue_dots, blue_targets),
            run_time=3
        )
        self.wait(0.5)
        
        # Highlight clustering success
        self.play(FadeIn(circle_red), FadeIn(circle_blue))
        
        # Show formula
        self.play(FadeIn(formula))
        self.wait(2)