from manim import *
import numpy as np
import random

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Manual Coordinate System (Replacing Axes/NumberPlane)
        x_axis = Line(LEFT * 5, RIGHT * 5, color=WHITE, stroke_width=1)
        y_axis = Line(DOWN * 3, UP * 3, color=WHITE, stroke_width=1)
        coords = VGroup(x_axis, y_axis)

        # 2. Country Outline (Simplified Australia shape)
        country_points = [
            [-3, 0.5, 0], [-2, 1.5, 0], [1, 1.2, 0], [3, 0.5, 0], 
            [3.5, -1.5, 0], [1, -2, 0], [-1.5, -2, 0], [-3, -1, 0]
        ]
        country = Polygon(*country_points, color=YELLOW, fill_opacity=0.1)

        # 3. Data points (gray dots)
        num_points = 60
        dots = VGroup()
        for _ in range(num_points):
            px = random.uniform(-2.5, 2.5)
            py = random.uniform(-1.5, 1.0)
            dots.add(Dot(point=[px, py, 0], color=GRAY, radius=0.07))

        # 4. Custom Cross Function (Replacing Cross)
        def get_cross(pos, color):
            size = 0.2
            l1 = Line(pos + UL * size, pos + DR * size, color=color, stroke_width=6)
            l2 = Line(pos + UR * size, pos + DL * size, color=color, stroke_width=6)
            return VGroup(l1, l2)

        # Centroids setup
        centroid_colors = [RED, GREEN, BLUE]
        centroid_positions = [
            [1.5, 1.5, 0],
            [-2.0, -1.0, 0],
            [0.5, -2.0, 0]
        ]
        centroids = VGroup(*[
            get_cross(pos, centroid_colors[i]) 
            for i, pos in enumerate(centroid_positions)
        ])

        # Formula and Labels
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            font_size=36
        ).to_edge(UP)
        
        label_data = Text("Continuous Coordinates", font_size=24).to_edge(LEFT, buff=0.5).shift(UP*2.5)
        label_target = Text("Discrete Regions", font_size=24, color=YELLOW).to_edge(RIGHT, buff=0.5).shift(UP*2.5)

        # --- ANIMATION ---

        # Show Initial Space
        self.play(Create(coords), Create(country))
        self.play(FadeIn(dots, lag_ratio=0.05), Write(label_data))
        self.wait(1)

        # Introduce Centroids and Formula
        self.play(Write(formula))
        self.play(AnimationGroup(*[Create(c) for c in centroids], lag_ratio=0.2))
        self.wait(1)

        # Assignment Step
        coloring_anims = []
        clusters = [[] for _ in range(len(centroids))]
        
        for dot in dots:
            dot_pos = dot.get_center()
            distances = [np.linalg.norm(dot_pos - c.get_center()) for c in centroids]
            nearest_idx = np.argmin(distances)
            clusters[nearest_idx].append(dot)
            coloring_anims.append(dot.animate.set_color(centroid_colors[nearest_idx]))
        
        self.play(*coloring_anims, run_time=2)
        self.wait(1)

        # Update Step (Move centroids to mean of their clusters)
        move_anims = []
        for i, cluster_dots in enumerate(clusters):
            if cluster_dots:
                positions = [d.get_center() for d in cluster_dots]
                mean_pos = np.mean(positions, axis=0)
                move_anims.append(centroids[i].animate.move_to(mean_pos))

        self.play(FadeOut(label_data), Write(label_target))
        self.play(*move_anims, run_time=2)
        
        # Highlight final targets
        self.play(
            *[c.animate.scale(1.3) for c in centroids]
        )
        self.wait(2)