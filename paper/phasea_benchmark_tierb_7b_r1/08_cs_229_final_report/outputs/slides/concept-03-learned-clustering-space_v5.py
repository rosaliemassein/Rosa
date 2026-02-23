from manim import *
import numpy as np

class LearnedClusteringSpace(Scene):
    def construct(self):
        # 1. Layout primitives (avoiding Axes/NumberPlane as they are disallowed)
        left_boundary = Rectangle(width=5.5, height=5.5, color=GRAY).shift(3.5 * LEFT)
        right_boundary = Rectangle(width=5.5, height=5.5, color=GRAY).shift(3.5 * RIGHT)
        
        # 2. Titles and labels
        physical_title = Tex("Physical Space").next_to(left_boundary, UP)
        learned_title = Tex("Learned Space").next_to(right_boundary, UP)
        
        # 3. Hits in Physical Space (heavily overlapping)
        # We use explicit coordinates based on center points to ensure clarity
        phys_center = 3.5 * LEFT
        dots_red = VGroup(*[
            Dot(color=RED, radius=0.08).move_to(
                phys_center + np.array([0.6 * np.cos(i), 0.6 * np.sin(i*1.2), 0])
            ) for i in range(20)
        ])
        dots_yellow = VGroup(*[
            Dot(color=YELLOW, radius=0.08).move_to(
                phys_center + np.array([0.5 * np.sin(i*1.5), 0.5 * np.cos(i), 0])
            ) for i in range(20)
        ])
        
        # 4. Hits in Learned Space (distinct and separable)
        # Cluster 1 moves to top-left of right box, Cluster 2 moves to bottom-right
        learned_center_1 = 3.5 * RIGHT + 1.2 * UP + 1.2 * LEFT
        learned_center_2 = 3.5 * RIGHT + 1.2 * DOWN + 1.2 * RIGHT
        
        target_red = VGroup(*[
            Dot(color=RED, radius=0.08).move_to(
                learned_center_1 + np.array([0.7 * np.cos(i), 0.7 * np.sin(i*1.2), 0])
            ) for i in range(20)
        ])
        target_yellow = VGroup(*[
            Dot(color=YELLOW, radius=0.08).move_to(
                learned_center_2 + np.array([0.7 * np.sin(i*1.5), 0.7 * np.cos(i), 0])
            ) for i in range(20)
        ])
        
        # 5. Success Markers (Standard circles since DashedVMobject is disallowed)
        success_circle_1 = Circle(radius=1.2, color=BLUE).move_to(learned_center_1)
        success_circle_2 = Circle(radius=1.2, color=BLUE).move_to(learned_center_2)
        
        # 6. Formula
        formula = MathTex(
            r"L_V = \frac{1}{N} \sum q_j \sum (\mathbb{1} \check{V}_k + (1-\mathbb{1}) \hat{V}_k)",
            font_size=32
        ).to_edge(DOWN)
        
        # 7. Animation Sequence
        self.add(left_boundary, right_boundary, physical_title, learned_title)
        self.play(FadeIn(dots_red), FadeIn(dots_yellow))
        self.wait(1)
        
        # Transformation from physical coordinates to learned space
        self.play(
            Transform(dots_red, target_red),
            Transform(dots_yellow, target_yellow),
            run_time=2.5
        )
        self.wait(0.5)
        
        # Clustering indicators
        self.play(Create(success_circle_1), Create(success_circle_2))
        self.play(Write(formula))
        self.wait(2)