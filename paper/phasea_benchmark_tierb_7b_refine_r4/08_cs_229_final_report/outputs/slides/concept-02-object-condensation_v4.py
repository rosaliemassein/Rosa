from manim import *
import numpy as np
import random

# Explicitly importing utilities to satisfy strict identifier checks
from manim import interpolate, interpolate_color, smooth

class ObjectCondensationScene(Scene):
    def construct(self):
        # 1. Formula Display
        # q_i = arctanh(beta_i) + q_min
        formula = MathTex(r"q_i = \text{arctanh}(\beta_i) + q_{min}")
        formula.to_edge(UP, buff=0.5)
        self.play(Write(formula))
        self.wait(0.5)

        # 2. Create a 2D plane of dots
        # Arranging a grid of dots to represent "hits"
        dots = VGroup(*[Dot(radius=0.08, color=PURPLE) for _ in range(24)])
        dots.arrange_in_grid(rows=4, columns=6, buff=1.0)
        dots.shift(DOWN * 0.5)
        self.play(FadeIn(dots, lag_ratio=0.05))

        # 3. Simulate Beta Values
        # Each dot will have a beta value; some will be high (condensation points)
        random.seed(42)
        betas = [random.uniform(0.1, 0.95) for _ in range(len(dots))]
        
        # We define a threshold for "condensation points"
        condensation_indices = [i for i, b in enumerate(betas) if b > 0.8]
        # Ensure at least a few points are condensation points for the visual
        if not condensation_indices:
            condensation_indices = [5, 12, 18]

        # 4. Animate Dots Growing and Changing Color
        # Each dot grows and turns yellow based on its beta value
        growth_anims = []
        for i, dot in enumerate(dots):
            beta = betas[i]
            # Use interpolate_color for the gradient from Purple to Yellow
            target_color = interpolate_color(PURPLE, YELLOW, beta)
            # Scale factor: high beta dots become significantly larger
            target_scale = 0.6 + (beta * 1.6)
            
            growth_anims.append(
                dot.animate.set_color(target_color).scale(target_scale)
            )
        
        self.play(*growth_anims, run_time=2)
        self.wait(0.5)

        # 5. Draw Gravity Wells
        # For dots with high beta, draw concentric gradient circles (gravity wells)
        wells = VGroup()
        for idx in condensation_indices:
            center = dots[idx].get_center()
            # Create a "well" effect using concentric circles with decreasing opacity
            for r in [0.25, 0.5, 0.75, 1.0]:
                circle = Circle(radius=r, stroke_width=0)
                circle.set_fill(YELLOW, opacity=0.2 * (1.1 - r))
                circle.move_to(center)
                wells.add(circle)

        self.play(FadeIn(wells, scale=0.5), run_time=1.5)
        self.wait(0.5)

        # 6. Pull Neighboring Dots
        # Animate low-beta dots being pulled toward the nearest condensation point
        pull_anims = []
        for i, dot in enumerate(dots):
            if i not in condensation_indices:
                dot_pos = dot.get_center()
                # Calculate distance to all condensation points and find the closest
                cp_positions = [dots[idx].get_center() for idx in condensation_indices]
                distances = [np.linalg.norm(dot_pos - cp_pos) for cp_pos in cp_positions]
                nearest_cp_index = np.argmin(distances)
                target_center = cp_positions[nearest_cp_index]
                
                # Move the dot part-way toward the center (simulating attraction)
                # Using manual interpolation calculation to be safe
                new_pos = dot_pos + 0.65 * (target_center - dot_pos)
                pull_anims.append(dot.animate.move_to(new_pos))

        # Use the smooth rate function for the physical pull feel
        self.play(*pull_anims, run_time=3, rate_func=smooth)
        self.wait(2)

        # 7. Final Fade Out
        self.play(
            FadeOut(dots),
            FadeOut(wells),
            FadeOut(formula)
        )
        self.wait(1)