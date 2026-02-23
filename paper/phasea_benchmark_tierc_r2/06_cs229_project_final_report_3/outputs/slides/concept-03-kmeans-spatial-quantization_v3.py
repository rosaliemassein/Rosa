from manim import *
import numpy as np

class KMeansSpatialQuantization(Scene):
    def construct(self):
        # 1. Background Setup: NumberPlane and Australia Outline
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.2}
        )
        self.add(plane)

        # A polygon approximating Australia's shape
        australia_points = [
            [2.5, 1.5, 0], [3.5, 0.5, 0], [4.5, 0.5, 0], [5.0, -0.5, 0],
            [4.5, -2.5, 0], [1.5, -3.0, 0], [-1.0, -2.5, 0], [-2.0, -1.0, 0],
            [-2.5, 0.5, 0], [-1.5, 1.5, 0], [0, 1.0, 0], [1.5, 2.0, 0]
        ]
        australia = Polygon(*australia_points, color=WHITE, stroke_width=2, fill_opacity=0.1)
        self.play(Create(australia))

        # 2. Data Points (Grey Dots)
        num_points = 200
        points_list = []
        while len(points_list) < num_points:
            p = [np.random.uniform(-3, 5.5), np.random.uniform(-3.5, 2.5), 0]
            # Simple check to keep points roughly within the map area
            if p[0] > -2.5 and p[0] < 5.0 and p[1] > -3.0 and p[1] < 2.0:
                points_list.append(Dot(p, radius=0.04, color=GRAY, fill_opacity=0.7))
        
        points_group = VGroup(*points_list)
        self.play(FadeIn(points_group, lag_ratio=0.01))

        # 3. Formula and Narration Text
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            color=YELLOW
        ).scale(0.8).to_edge(UP)
        
        voice_text = Text(
            "Discretizing continuous coordinates into predictable regions.",
            font_size=24
        ).to_edge(DOWN)

        # 4. Centroids Initialization (Manual Cross creation)
        def create_centroid_cross(color):
            cross = VGroup(
                Line(UL, DR),
                Line(UR, DL)
            ).scale(0.15).set_stroke(color=color, width=5)
            return cross

        num_clusters = 4
        colors = [BLUE, GREEN, RED, ORANGE]
        centroid_positions = [
            [0, 0, 0], [3, 1, 0], [-1, -2, 0], [4, -2, 0]
        ]
        centroids = VGroup(*[
            create_centroid_cross(colors[i]).move_to(pos)
            for i, pos in enumerate(centroid_positions)
        ])

        self.play(Write(formula), Write(voice_text))
        self.play(Create(centroids))
        self.wait(1)

        # 5. K-Means Iteration Loop
        for iteration in range(3):
            # Step A: Assignment (Color points based on nearest centroid)
            animations = []
            clusters = [[] for _ in range(num_clusters)]
            
            for pt in points_group:
                # Calculate distance to each centroid marker's center
                distances = [np.linalg.norm(pt.get_center() - c.get_center()) for c in centroids]
                closest_idx = np.argmin(distances)
                clusters[closest_idx].append(pt)
                animations.append(pt.animate.set_color(colors[closest_idx]))
            
            self.play(*animations, run_time=1)
            self.wait(0.5)

            # Step B: Update (Move centroids to center of their respective colored groups)
            move_anims = []
            for i, cluster_pts in enumerate(clusters):
                if not cluster_pts:
                    continue
                new_mean = np.mean([p.get_center() for p in cluster_pts], axis=0)
                move_anims.append(centroids[i].animate.move_to(new_mean))
            
            self.play(*move_anims, run_time=1.5)
            self.wait(0.5)

        # 6. Conclusion
        conclusion_text = Text(
            "Regression problem turned into classification task.",
            font_size=24
        ).to_edge(DOWN)
        
        self.play(
            centroids.animate.scale(1.2),
            formula.animate.set_color(WHITE),
            Transform(voice_text, conclusion_text)
        )
        
        # Final highlight of discrete targets
        rects = VGroup(*[SurroundingRectangle(c, color=c[0].get_color(), buff=0.1) for c in centroids])
        self.play(Create(rects))
        self.wait(2)