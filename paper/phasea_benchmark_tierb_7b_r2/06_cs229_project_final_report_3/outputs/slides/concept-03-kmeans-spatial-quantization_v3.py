from manim import *
import numpy as np

class KMeansSpatialQuantization(Scene):
    def construct(self):
        # Instead of NumberPlane (which is disallowed), draw a simple grid with lines
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line(start=[x, -4, 0], end=[x, 4, 0], stroke_opacity=0.15, stroke_width=1))
        for y in range(-4, 5):
            grid.add(Line(start=[-7, y, 0], end=[7, y, 0], stroke_opacity=0.15, stroke_width=1))
        self.add(grid)

        # Simplified Australia outline
        australia_points = [
            [-3, 1, 0], [-1, 1.5, 0], [1, 1, 0], [1.5, -0.5, 0],
            [1, -1.5, 0], [-1, -2, 0], [-3, -1.5, 0], [-3.5, -0.5, 0]
        ]
        australia = Polygon(*australia_points, color=BLUE, fill_opacity=0.1)
        self.play(Create(australia))
        
        # Populate with data points (Gray dots)
        np.random.seed(42)
        dots_list = []
        for _ in range(80):
            # Coordinates roughly inside the "Australia" polygon
            p = [np.random.uniform(-3.2, 1.2), np.random.uniform(-1.8, 1.2), 0]
            dots_list.append(Dot(point=p, radius=0.06, color=GRAY))
        
        data_points = VGroup(*dots_list)
        self.play(FadeIn(data_points, lag_ratio=0.05))
        self.wait(0.5)

        # Define centroids (manual Cross since Cross is undefined)
        def get_cross(pos, color):
            return VGroup(
                Line([-0.15, -0.15, 0], [0.15, 0.15, 0]),
                Line([-0.15, 0.15, 0], [0.15, -0.15, 0])
            ).move_to(pos).set_color(color).set_stroke(width=4)

        centroid_colors = [RED, YELLOW, GREEN]
        current_centers = [
            np.array([-2.5, 0.5, 0]),
            np.array([0.5, 0.8, 0]),
            np.array([-0.5, -1.0, 0])
        ]
        
        centroids = VGroup(*[get_cross(current_centers[i], centroid_colors[i]) for i in range(3)])
        self.play(Create(centroids))
        self.wait(0.5)

        # K-means convergence animation (2 iterations)
        for iteration in range(2):
            # Assignment Step: Color dots based on proximity
            coloring_anims = []
            clusters = [[] for _ in range(3)]
            
            for dot in data_points:
                dists = [np.linalg.norm(dot.get_center() - center) for center in current_centers]
                nearest_idx = np.argmin(dists)
                clusters[nearest_idx].append(dot)
                coloring_anims.append(dot.animate.set_color(centroid_colors[nearest_idx]))
            
            self.play(*coloring_anims, run_time=1)
            
            # Update Step: Move centroids to the mean of their clusters
            move_anims = []
            for i in range(3):
                if clusters[i]:
                    new_pos = np.mean([d.get_center() for d in clusters[i]], axis=0)
                    current_centers[i] = new_pos
                    move_anims.append(centroids[i].animate.move_to(new_pos))
            
            self.play(*move_anims, run_time=1)
            self.wait(0.5)

        # Final labels and Formula
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}"
        ).scale(0.85).to_edge(DOWN, buff=0.4)
        
        # Manually create background for formula since BackgroundRectangle is undefined
        formula_bg = Rectangle(
            width=formula.width + 0.5,
            height=formula.height + 0.4,
            fill_color=BLACK,
            fill_opacity=0.8,
            stroke_width=0
        ).move_to(formula)
        
        self.play(FadeIn(formula_bg), Write(formula))
        
        # Highlight final regions
        self.play(centroids.animate.scale(1.2))
        self.wait(2)