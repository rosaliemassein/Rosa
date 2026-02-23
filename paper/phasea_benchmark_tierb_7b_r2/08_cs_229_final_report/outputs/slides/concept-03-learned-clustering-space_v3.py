from manim import *

class Concept03LearningClusteringSpace(Scene):
    def construct(self):
        # 1. Setup Physical Space (Left)
        # Using Line instead of Axes/NumberPlane to comply with constraints
        p_center = LEFT * 3.5
        p_x_axis = Line(p_center + LEFT * 2, p_center + RIGHT * 2, color=WHITE)
        p_y_axis = Line(p_center + DOWN * 2, p_center + UP * 2, color=WHITE)
        p_label = Text("Physical Space", font_size=24).next_to(p_x_axis, UP, buff=1.8)
        p_group = VGroup(p_x_axis, p_y_axis, p_label)

        # 2. Setup Learned Space (Right)
        l_center = RIGHT * 3.5
        l_x_axis = Line(l_center + LEFT * 2, l_center + RIGHT * 2, color=WHITE)
        l_y_axis = Line(l_center + DOWN * 2, l_center + UP * 2, color=WHITE)
        l_label = Text("Learned Space", font_size=24).next_to(l_x_axis, UP, buff=1.8)
        l_group = VGroup(l_x_axis, l_y_axis, l_label)

        # 3. Reference Formula
        formula = MathTex(
            r"L_V = \frac{1}{N} \sum q_j \sum (\mathbb{1} \check{V}_k + (1-\mathbb{1}) \hat{V}_k)",
            font_size=24
        ).to_edge(DOWN, buff=0.5)

        # 4. Create Overlapping Hits in Physical Space
        # Cluster 1 (Red)
        red_p = VGroup(
            Dot(p_center + 0.2*RIGHT + 0.3*UP, color=RED, radius=0.08),
            Dot(p_center + 0.4*RIGHT + 0.1*UP, color=RED, radius=0.08),
            Dot(p_center - 0.1*RIGHT + 0.4*UP, color=RED, radius=0.08),
            Dot(p_center + 0.3*RIGHT - 0.2*UP, color=RED, radius=0.08),
            Dot(p_center - 0.2*RIGHT - 0.1*UP, color=RED, radius=0.08)
        )
        # Cluster 2 (Blue) - Heavily overlapping
        blue_p = VGroup(
            Dot(p_center + 0.1*RIGHT + 0.2*UP, color=BLUE, radius=0.08),
            Dot(p_center + 0.3*RIGHT + 0.3*UP, color=BLUE, radius=0.08),
            Dot(p_center - 0.2*RIGHT + 0.2*UP, color=BLUE, radius=0.08),
            Dot(p_center + 0.1*RIGHT - 0.3*UP, color=BLUE, radius=0.08),
            Dot(p_center - 0.3*RIGHT - 0.2*UP, color=BLUE, radius=0.08)
        )
        physical_dots = VGroup(red_p, blue_p)

        # 5. Define Targets in Learned Space (Separated)
        # Red moves left, Blue moves right
        red_l = VGroup(
            Dot(l_center + LEFT + 0.2*RIGHT + 0.3*UP, color=RED, radius=0.08),
            Dot(l_center + LEFT + 0.4*RIGHT + 0.1*UP, color=RED, radius=0.08),
            Dot(l_center + LEFT - 0.1*RIGHT + 0.4*UP, color=RED, radius=0.08),
            Dot(l_center + LEFT + 0.3*RIGHT - 0.2*UP, color=RED, radius=0.08),
            Dot(l_center + LEFT - 0.2*RIGHT - 0.1*UP, color=RED, radius=0.08)
        )
        blue_l = VGroup(
            Dot(l_center + RIGHT + 0.1*RIGHT + 0.2*UP, color=BLUE, radius=0.08),
            Dot(l_center + RIGHT + 0.3*RIGHT + 0.3*UP, color=BLUE, radius=0.08),
            Dot(l_center + RIGHT - 0.2*RIGHT + 0.2*UP, color=BLUE, radius=0.08),
            Dot(l_center + RIGHT + 0.1*RIGHT - 0.3*UP, color=BLUE, radius=0.08),
            Dot(l_center + RIGHT - 0.3*RIGHT - 0.2*UP, color=BLUE, radius=0.08)
        )
        learned_dots = VGroup(red_l, blue_l)

        # 6. Animation sequence
        self.add(p_group)
        self.play(FadeIn(physical_dots, lag_ratio=0.1))
        self.wait(1)

        self.play(
            Create(l_group),
            Write(formula)
        )
        self.wait(1)

        # Transformation to Learned Space
        self.play(
            Transform(physical_dots, learned_dots),
            run_time=3,
            path_arc=0.3
        )
        self.wait(0.5)

        # Classification circles
        c1 = Circle(radius=0.9, color=YELLOW).move_to(l_center + LEFT)
        c2 = Circle(radius=0.9, color=YELLOW).move_to(l_center + RIGHT)
        
        # Simulating dashed effect with stroke settings if supported, or just solid circles
        c1.set_stroke(width=2)
        c2.set_stroke(width=2)

        self.play(Create(c1), Create(c2))
        self.wait(2)