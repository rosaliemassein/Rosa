from manim import *
import numpy as np

class KMeansSpatialQuantization(Scene):
    def construct(self):
        # 1. Custom Coordinate System (using basic Lines as Axes is disallowed)
        x_axis = Line(5 * LEFT, 5 * RIGHT, color=BLUE, stroke_width=2)
        y_axis = Line(3 * DOWN, 3 * UP, color=BLUE, stroke_width=2)
        axes_group = VGroup(x_axis, y_axis)
        
        # 2. Country Outline (Simplified Australia-like)
        # Using a polygon for the country outline
        outline_coords = [
            [-3.5, 1, 0], [-2, 1.5, 0], [0, 1.2, 0], [2, 1.5, 0], 
            [3.5, 0.5, 0], [3.8, -1.5, 0], [2, -2.5, 0], [0, -2, 0], 
            [-2.5, -2.5, 0], [-3.8, -1, 0]
        ]
        country = Polygon(*outline_coords, color=GREEN, fill_opacity=0.1)
        
        self.play(Create(axes_group), Create(country))
        self.wait(0.5)

        # 3. Training coordinates (Data Points)
        dots = VGroup()
        for _ in range(80):
            # Generate random points inside the general area
            px = np.random.uniform(-3, 3)
            py = np.random.uniform(-2, 1)
            dots.add(Dot(point=[px, py, 0], radius=0.04, color=GRAY))
        
        self.play(FadeIn(dots, lag_ratio=0.01))
        self.wait(0.5)

        # 4. Centroid 'Crosses' (mu_j)
        cluster_colors = [RED, YELLOW, BLUE]
        
        def create_cross(color_val):
            l1 = Line([-0.15, -0.15, 0], [0.15, 0.15, 0], color=color_val, stroke_width=4)
            l2 = Line([-0.15, 0.15, 0], [0.15, -0.15, 0], color=color_val, stroke_width=4)
            return VGroup(l1, l2)

        centroids = VGroup(*[create_cross(c) for c in cluster_colors])
        
        # Initial positions
        init_positions = [[-2, 0, 0], [0, -1, 0], [2, 0.5, 0]]
        for i, c in enumerate(centroids):
            c.move_to(init_positions[i])
        
        self.play(AnimationGroup(*[FadeIn(c) for c in centroids], lag_ratio=0.3))
        self.wait(0.5)

        # 5. K-means Formula
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            font_size=36
        ).to_corner(UL).set_stroke(BLACK, 4, background=True)
        self.play(Write(formula))
        self.wait(0.5)

        # 6. K-Means Algorithm Iterations
        for iteration in range(3):
            # Step A: Assignment
            assignment_anims = []
            for d in dots:
                d_pos = d.get_center()
                # Find index of closest centroid
                dists = [np.linalg.norm(d_pos - c.get_center()) for c in centroids]
                closest_idx = np.argmin(dists)
                d.target_color = cluster_colors[closest_idx]
                d.target_cluster = closest_idx
                assignment_anims.append(d.animate.set_color(d.target_color))
            
            self.play(*assignment_anims, run_time=1.2)
            self.wait(0.3)

            # Step B: Update
            move_anims = []
            for i in range(len(centroids)):
                # Filter points in cluster i
                pts = [d.get_center() for d in dots if d.target_cluster == i]
                if pts:
                    new_pos = np.mean(pts, axis=0)
                    move_anims.append(centroids[i].animate.move_to(new_pos))
            
            if move_anims:
                self.play(*move_anims, run_time=1.2)
            self.wait(0.3)

        # 7. Final Highlighting
        self.play(
            centroids.animate.scale(1.5),
            dots.animate.set_opacity(0.4),
            formula.animate.set_color(YELLOW)
        )
        self.wait(2)