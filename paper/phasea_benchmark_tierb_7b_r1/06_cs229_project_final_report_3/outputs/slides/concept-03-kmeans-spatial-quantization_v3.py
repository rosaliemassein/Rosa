import numpy as np
from manim import *

class KMeansSpatialQuantization(Scene):
    def construct(self):
        # 1. Background context (manual coordinate lines to avoid restricted Axes/NumberPlane)
        h_line = Line(LEFT * 7, RIGHT * 7, color=GREY_E, stroke_width=1)
        v_line = Line(UP * 4, DOWN * 4, color=GREY_E, stroke_width=1)
        self.add(h_line, v_line)

        # 2. Draw Australia-like outline (Simplified Polygon)
        australia_points = [
            [-4, 0, 0], [-3, 1.5, 0], [-1.2, 2.2, 0], [1.5, 2, 0], 
            [4, 1.2, 0], [4.5, -1, 0], [3, -2.8, 0], [0.5, -2.5, 0], 
            [-2.5, -2, 0], [-4, 0, 0]
        ]
        australia = Polygon(*australia_points, color=YELLOW, stroke_width=4)
        self.play(Create(australia))

        # 3. Generate random data points (discretizing continuous space)
        np.random.seed(42)
        raw_coords = []
        for _ in range(120):
            # Box containing the outline
            px = np.random.uniform(-3.5, 4)
            py = np.random.uniform(-2.2, 1.8)
            raw_coords.append([px, py, 0])
        
        data_points = VGroup(*[Dot(p, radius=0.04, color=GRAY) for p in raw_coords])
        self.play(FadeIn(data_points))

        # 4. Create Centroid markers (mu_j)
        def create_centroid_marker(pos, color):
            # Manual cross since 'Cross' might be undefined in this environment
            l1 = Line(pos + [-0.2, -0.2, 0], pos + [0.2, 0.2, 0], color=color, stroke_width=6)
            l2 = Line(pos + [-0.2, 0.2, 0], pos + [0.2, -0.2, 0], color=color, stroke_width=6)
            return VGroup(l1, l2)

        initial_centroid_pos = [
            np.array([-2.2, 1.2, 0]),
            np.array([2.8, 1.3, 0]),
            np.array([2.2, -1.8, 0]),
            np.array([-1.8, -1.3, 0])
        ]
        centroid_colors = [RED, BLUE, GREEN, ORANGE]
        centroids = VGroup(*[
            create_centroid_marker(initial_centroid_pos[i], centroid_colors[i]) 
            for i in range(4)
        ])
        
        self.play(AnimationGroup(*[Create(c) for c in centroids], lag_ratio=0.2))
        self.wait(0.5)

        # 5. Cluster Assignment (Voronoi coloring)
        clusters = [[] for _ in range(4)]
        coloring_anims = []
        for dp in data_points:
            dists = [np.linalg.norm(dp.get_center() - cp) for cp in initial_centroid_pos]
            nearest_idx = np.argmin(dists)
            clusters[nearest_idx].append(dp)
            coloring_anims.append(dp.animate.set_color(centroid_colors[nearest_idx]))
        
        self.play(*coloring_anims, run_time=1.5)
        self.wait(0.5)

        # 6. Show the update formula
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            font_size=32
        ).to_edge(UP, buff=0.3).set_stroke(BLACK, 4, background=True)
        self.play(Write(formula))

        # 7. Update step: move centroids to group centers
        movement_anims = []
        final_pos_list = []
        for i in range(4):
            if clusters[i]:
                new_mu = np.mean([d.get_center() for d in clusters[i]], axis=0)
            else:
                new_mu = initial_centroid_pos[i]
            final_pos_list.append(new_mu)
            movement_anims.append(centroids[i].animate.move_to(new_mu))

        self.play(*movement_anims, run_time=2)
        self.wait(0.5)

        # 8. Highlight final cluster centers as targets
        targets = VGroup(*[
            Circle(radius=0.3, color=WHITE).move_to(p) for p in final_pos_list
        ])
        self.play(Create(targets))
        self.play(targets.animate.scale(1.2).set_stroke(opacity=0), run_time=0.8)
        
        self.wait(2)