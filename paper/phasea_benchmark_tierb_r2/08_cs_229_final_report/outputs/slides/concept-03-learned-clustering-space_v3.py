from manim import *
import numpy as np

class LearnedClusteringSpace(Scene):
    def construct(self):
        # 1. Manual Axis Construction (to avoid NumberPlane/Axes errors)
        # Left side: Physical Space
        left_origin = 3.5 * LEFT
        l_x_axis = Line(left_origin + 2.5 * LEFT, left_origin + 2.5 * RIGHT, color=GREY)
        l_y_axis = Line(left_origin + 2.5 * DOWN, left_origin + 2.5 * UP, color=GREY)
        l_label = Text("Physical Space", font_size=24).move_to(left_origin + 3 * UP)
        
        # Right side: Learned Space
        right_origin = 3.5 * RIGHT
        r_x_axis = Line(right_origin + 2.5 * LEFT, right_origin + 2.5 * RIGHT, color=GREY)
        r_y_axis = Line(right_origin + 2.5 * DOWN, right_origin + 2.5 * UP, color=GREY)
        r_label = Text("Learned Space", font_size=24).move_to(right_origin + 3 * UP)

        # 2. Points (Hits) Generation
        num_points = 15
        red_start_pos = []
        yel_start_pos = []
        red_end_pos = []
        yel_end_pos = []
        
        # Seed for consistent distribution
        np.random.seed(42)
        
        for i in range(num_points):
            # Physical Space: Overlapping distributions
            # Cluster A (Red) centered slightly left of physical origin
            rx = -3.8 + np.random.normal(0, 0.4)
            ry = 0.0 + np.random.normal(0, 0.4)
            red_start_pos.append([rx, ry, 0])
            
            # Cluster B (Yellow) centered slightly right of physical origin
            yx = -3.2 + np.random.normal(0, 0.4)
            yy = 0.0 + np.random.normal(0, 0.4)
            yel_start_pos.append([yx, yy, 0])
            
            # Learned Space: Separated distributions
            # Cluster A (Red) at top of learned space
            rex = 3.5 + np.random.normal(0, 0.5)
            rey = 1.5 + np.random.normal(0, 0.5)
            red_end_pos.append([rex, rey, 0])
            
            # Cluster B (Yellow) at bottom of learned space
            yex = 3.5 + np.random.normal(0, 0.5)
            yey = -1.5 + np.random.normal(0, 0.5)
            yel_end_pos.append([yex, yey, 0])

        # Create Dot objects
        red_dots = VGroup(*[Dot(p, color=RED, radius=0.07) for p in red_start_pos])
        yel_dots = VGroup(*[Dot(p, color=YELLOW, radius=0.07) for p in yel_start_pos])

        # 3. Classification Boundaries
        # Using standard Circle since DashedVMobject was flagged
        circ_a = Circle(radius=1.2, color=RED).move_to(right_origin + 1.5 * UP)
        circ_b = Circle(radius=1.2, color=YELLOW).move_to(right_origin + 1.5 * DOWN)
        
        # 4. Formula
        formula = MathTex(
            r"L_V = \frac{1}{N} \sum q_j \sum (\mathbb{1} \check{V}_k + (1-\mathbb{1}) \hat{V}_k)",
            font_size=30
        ).to_edge(DOWN, buff=0.5)

        # --- Animation Sequence ---
        
        # Initial Scene Setup
        self.add(l_x_axis, l_y_axis, l_label, r_x_axis, r_y_axis, r_label)
        self.play(FadeIn(red_dots), FadeIn(yel_dots))
        self.wait(1)
        
        # Transformation from Physical to Learned Space
        # Each dot is mapped from its physical coordinate to its learned coordinate
        self.play(
            *[red_dots[i].animate.move_to(red_end_pos[i]) for i in range(num_points)],
            *[yel_dots[i].animate.move_to(yel_end_pos[i]) for i in range(num_points)],
            run_time=3
        )
        self.wait(0.5)
        
        # Final classification markers and formula
        self.play(Create(circ_a), Create(circ_b))
        self.play(Write(formula))
        self.wait(2)