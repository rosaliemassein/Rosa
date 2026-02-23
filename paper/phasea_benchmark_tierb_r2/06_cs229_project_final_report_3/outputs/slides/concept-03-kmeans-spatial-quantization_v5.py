from manim import *
import numpy as np

class KMeansSpatialQuantization(Scene):
    def construct(self):
        # 1. Voice narration and goal setup
        voice_text = (
            "Predicting exact latitude and longitude is incredibly difficult because coordinates are continuous and high-variance. "
            "To solve this, we simplify the problem using spatial clustering. Within each country, we group our training coordinates into K clusters. "
            "Instead of asking the model to guess any point on the map, we ask it to classify which 'region' or cluster the image belongs to."
        )
        voice = Text(voice_text, color=BLUE).scale(0.4).to_edge(UP)
        self.play(Write(voice), run_time=4)
        self.wait(1)

        # 2. Setup a Grid (replacing NumberPlane)
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line([x, -4, 0], [x, 4, 0], color=GRAY, stroke_width=1, stroke_opacity=0.3))
        for y in range(-4, 5):
            grid.add(Line([-7, y, 0], [7, y, 0], color=GRAY, stroke_width=1, stroke_opacity=0.3))
        self.play(Create(grid))

        # 3. Draw outline of Australia
        australia_points = [
            [-3, 1.5, 0], [-1.5, 2, 0], [1.5, 1.8, 0], [3.5, 0.5, 0], 
            [3, -1.5, 0], [1, -2.5, 0], [-1, -2.2, 0], [-3.2, -1.2, 0], [-3, 1.5, 0]
        ]
        australia_outline = Polygon(*australia_points, color=RED, stroke_width=4)
        self.play(Create(australia_outline))

        # 4. Generate data points (Gray dots)
        dots = VGroup()
        for _ in range(120):
            # Simple bounding box random placement
            p = [np.random.uniform(-3, 3), np.random.uniform(-2, 1.5), 0]
            dots.add(Dot(p, radius=0.05, color=GRAY))
        self.play(FadeIn(dots, lag_ratio=0.05))
        self.wait()

        # 5. Define Custom Cross (replacing undefined Cross)
        def get_custom_cross(color):
            return VGroup(
                Line(UL, DR, stroke_width=6),
                Line(UR, DL, stroke_width=6)
            ).scale(0.15).set_color(color)

        # 6. Centroid crosses (Initial random locations)
        k = 4
        colors = [YELLOW, BLUE, GREEN, ORANGE]
        centroids = VGroup()
        for i in range(k):
            pos = [np.random.uniform(-2, 2), np.random.uniform(-1, 1), 0]
            centroids.add(get_custom_cross(colors[i]).move_to(pos))
        
        self.play(Create(centroids))
        self.wait()

        # 7. Formula display
        formula_tex = r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}\mathbf{x}^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}"
        formula = MathTex(formula_tex).scale(0.7).to_corner(DL).set_backstroke(BLACK, width=8)
        self.play(Write(formula))

        # 8. K-means Iteration Logic
        def update_clusters(dots_vgroup, centroid_vgroup):
            assignments = []
            for dot in dots_vgroup:
                dists = [np.linalg.norm(dot.get_center() - c.get_center()) for c in centroid_vgroup]
                assignments.append(np.argmin(dists))
            return assignments

        # First Coloring based on proximity
        assignments = update_clusters(dots, centroids)
        self.play(*[dot.animate.set_color(colors[assignments[i]]) for i, dot in enumerate(dots)])
        self.wait(1)

        # Centroid movement to centers of groups
        for _ in range(2):
            new_moves = []
            for i in range(k):
                points_in_cluster = [dots[j].get_center() for j, cluster_idx in enumerate(assignments) if cluster_idx == i]
                if points_in_cluster:
                    mean_pos = np.mean(points_in_cluster, axis=0)
                    new_moves.append(centroids[i].animate.move_to(mean_pos))
            
            if new_moves:
                self.play(*new_moves)
            
            # Recalculate assignments and update colors
            assignments = update_clusters(dots, centroids)
            self.play(*[dot.animate.set_color(colors[assignments[i]]) for i, dot in enumerate(dots)])
            self.wait(0.5)

        # 9. Final Highlights
        self.play(FadeOut(voice))
        final_text = Text("Discrete 'Regions' for Classification", color=WHITE).scale(0.6).to_edge(UP)
        self.play(Write(final_text))
        self.play(*[Indicate(c, scale_factor=2) for c in centroids])
        self.wait(3)