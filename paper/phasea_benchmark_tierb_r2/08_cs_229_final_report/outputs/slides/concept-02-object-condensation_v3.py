from manim import *
import numpy as np
import random

class ObjectCondensation(Scene):
    def construct(self):
        # 1. Formula Display
        formula = MathTex(r"q_i = \text{arctanh}(\beta_i) + q_{min}")
        formula.to_edge(UP)
        self.play(Write(formula))

        # 2. Data Preparation
        # Define 3 condensation centers
        centers = [
            np.array([3, 1.5, 0]),
            np.array([-3, 1, 0]),
            np.array([0, -2, 0])
        ]
        
        points_data = []
        
        # Add high-beta dots (the condensation points)
        for cp_pos in centers:
            points_data.append({
                "pos": cp_pos,
                "beta": 0.95,
                "is_center": True
            })
            
        # Add 35 low-beta noise dots
        for _ in range(35):
            pos = np.array([
                random.uniform(-7, 7),
                random.uniform(-3, 3),
                0
            ])
            beta = random.uniform(0.1, 0.4)
            points_data.append({
                "pos": pos,
                "beta": beta,
                "is_center": False
            })

        # 3. Create Initial Mobjects
        dots = VGroup()
        for p in points_data:
            # All dots start as small purple dots
            dot = Dot(point=p["pos"], radius=0.08, color=PURPLE)
            p["mobject"] = dot
            dots.add(dot)

        self.add(dots)
        self.wait(1)

        # 4. Animation: Growth and Color Change
        # We manually map beta to colors to avoid interpolate_color issues
        growth_anims = []
        for p in points_data:
            if p["beta"] > 0.8:
                target_color = YELLOW
            elif p["beta"] > 0.5:
                target_color = ORANGE
            else:
                target_color = PURPLE
                
            # Dots with higher beta grow more
            target_scale = 1.0 + p["beta"] * 2.5
            growth_anims.append(
                p["mobject"].animate.scale(target_scale).set_color(target_color)
            )
            
        self.play(*growth_anims, run_time=2)
        self.wait(0.5)

        # 5. Animation: Gravity Wells (Potential Gradient)
        # We use concentric circles to visualize the potential around condensation points
        wells = VGroup()
        for cp_pos in centers:
            well_group = VGroup()
            for r in [0.4, 0.8, 1.2, 1.6, 2.0]:
                circle = Circle(radius=r, color=YELLOW, stroke_width=1.5)
                # Opacity decreases as radius increases
                circle.set_opacity(0.3 * (1 - (r / 2.2)))
                circle.move_to(cp_pos)
                well_group.add(circle)
            wells.add(well_group)
            
        self.play(FadeIn(wells, scale=0.5), run_time=1.5)
        self.wait(0.5)

        # 6. Animation: Noise dots being pulled toward the wells
        pull_anims = []
        for p in points_data:
            if not p["is_center"]:
                # Find the nearest condensation center
                best_center = centers[0]
                min_dist = np.linalg.norm(p["pos"] - centers[0])
                for cp_pos in centers:
                    d = np.linalg.norm(p["pos"] - cp_pos)
                    if d < min_dist:
                        min_dist = d
                        best_center = cp_pos
                
                # Calculate movement vector (moving 70% of the way to the center)
                move_vec = (best_center - p["pos"]) * 0.7
                pull_anims.append(
                    p["mobject"].animate.shift(move_vec)
                )
        
        # The default rate_func for play is smooth
        self.play(*pull_anims, run_time=3)
        self.wait(2)

        # Final cleanup
        self.play(FadeOut(dots), FadeOut(wells), FadeOut(formula))