from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Create a country-like outline (Australia approximation)
        outline_points = [
            [-3, 1.5, 0], [-2, 2, 0], [0, 1.8, 0], [2, 2.2, 0], 
            [3.5, 1.5, 0], [4, 0, 0], [3.5, -1.5, 0], [2, -2.5, 0], 
            [0, -2.8, 0], [-2, -2.5, 0], [-3.5, -1, 0], [-4, 0.5, 0]
        ]
        country = Polygon(*outline_points, color=WHITE, stroke_width=3)
        country.set_fill(BLUE, opacity=0.1)
        
        self.play(Create(country))
        self.wait(0.5)

        # 2. Populate with data points (gray dots)
        # We generate points and only keep those inside the polygon if possible, 
        # but for simplicity in this environment, we'll place them in a bounded box.
        data_points = VGroup()
        for _ in range(100):
            p = [np.random.uniform(-3.5, 3.5), np.random.uniform(-2.2, 1.8), 0]
            data_points.add(Dot(point=p, radius=0.05, color=GRAY))
        
        self.play(FadeIn(data_points, lag_ratio=0.01))
        self.wait(0.5)

        # 3. Create Centroid crosses (mu_j)
        centroid_colors = [RED, GREEN, YELLOW, ORANGE]
        # Initial random positions
        start_positions = [
            [-2, 1, 0], [2, 1, 0], [-1.5, -1.5, 0], [1.5, -1.2, 0]
        ]
        
        centroids = VGroup()
        for i in range(4):
            # A cross shape for mu_j
            cross = VGroup(
                Line(0.2 * LEFT + 0.2 * UP, 0.2 * RIGHT + 0.2 * DOWN),
                Line(0.2 * LEFT + 0.2 * DOWN, 0.2 * RIGHT + 0.2 * UP)
            ).set_color(centroid_colors[i]).move_to(start_positions[i])
            
            label = MathTex(f"\\mu_{i+1}", font_size=20).next_to(cross, UP, buff=0.1)
            centroids.add(VGroup(cross, label))

        self.play(LaggedStart(*[FadeIn(c) for c in centroids], lagged_ratio=0.3))
        self.wait(1)

        # 4. Nearest Centroid Assignment (Color dots)
        def get_dist(p1, p2):
            return np.linalg.norm(p1 - p2)

        point_groups = [[] for _ in range(4)]
        color_anims = []
        
        for dot in data_points:
            dists = [get_dist(dot.get_center(), c[0].get_center()) for c in centroids]
            closest_idx = np.argmin(dists)
            point_groups[closest_idx].append(dot)
            color_anims.append(dot.animate.set_color(centroid_colors[closest_idx]))
            
        self.play(*color_anims, run_time=1.5)
        self.wait(0.5)

        # 5. Show Formula
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            font_size=32
        ).to_edge(UP, buff=0.5)
        self.play(Write(formula))
        self.wait(1)

        # 6. Convergence: Move centroids to the mean of their groups
        move_anims = []
        for i in range(4):
            if point_groups[i]:
                group_points = [d.get_center() for d in point_groups[i]]
                mean_pos = np.mean(group_points, axis=0)
                move_anims.append(centroids[i].animate.move_to(mean_pos))
        
        self.play(*move_anims, run_time=2)
        self.wait(1)

        # 7. Final Highlight
        self.play(*[Indicate(c, color=WHITE) for c in centroids])
        self.wait(2)