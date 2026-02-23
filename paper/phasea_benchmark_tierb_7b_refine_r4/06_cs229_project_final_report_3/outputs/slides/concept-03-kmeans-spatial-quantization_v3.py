from manim import *
import numpy as np

class KMeansSpatialQuantization(Scene):
    def construct(self):
        # 1. Draw Australia Outline (Using simple Polygon)
        # Defining points manually to avoid complex geometry dependencies
        australia_points = [
            [-3, -1.5, 0], [-3.5, -0.5, 0], [-3.2, 0.8, 0], [-1.5, 1.2, 0], 
            [0, 1, 0], [1.5, 1.8, 0], [3, 1.3, 0], [3.5, -0.2, 0], 
            [3, -1.5, 0], [2, -2, 0], [0, -2.5, 0], [-2, -2.2, 0]
        ]
        outline = Polygon(*australia_points, color=WHITE, fill_opacity=0.3, fill_color=BLUE)
        self.play(Create(outline))
        self.wait(0.5)

        # 2. Populate with small gray dots
        np.random.seed(42)
        dots_list = []
        for _ in range(80):
            x = np.random.uniform(-3.2, 3.2)
            y = np.random.uniform(-2.2, 1.5)
            # Basic bounding box check for the randomized points
            dots_list.append(Dot(point=[x, y, 0], radius=0.06, color=GRAY))
        
        data_points = VGroup(*dots_list)
        self.play(FadeIn(data_points, lag_ratio=0.01), run_time=1.5)

        # 3. Create Custom Centroid (Replacement for undefined 'Cross')
        def create_centroid_marker(color):
            line1 = Line(np.array([-0.15, 0.15, 0]), np.array([0.15, -0.15, 0]), color=color, stroke_width=5)
            line2 = Line(np.array([-0.15, -0.15, 0]), np.array([0.15, 0.15, 0]), color=color, stroke_width=5)
            return VGroup(line1, line2)

        centroid_colors = [RED, GREEN, YELLOW]
        centroids = VGroup()
        # Random initial positions for centroids
        start_positions = [[-1.5, 0.5, 0], [1.5, 0.5, 0], [0, -1.5, 0]]
        for i in range(3):
            c = create_centroid_marker(centroid_colors[i])
            c.move_to(start_positions[i])
            centroids.add(c)
            
        self.play(AnimationGroup(*[Create(c) for c in centroids], lag_ratio=0.3))

        # 4. Display the K-means formula
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            font_size=32
        ).to_edge(UP, buff=0.2).add_background_rectangle()
        self.play(Write(formula))
        self.wait(1)

        # 5. K-means Iteration Logic
        def get_dist(p1, p2):
            return np.sqrt(np.sum((p1 - p2)**2))

        # Perform 2 iterations to show convergence
        for _ in range(2):
            # Assignment Step: Change dot colors based on nearest centroid
            assignment_anims = []
            clusters = [[] for _ in range(len(centroids))]
            
            for dot in data_points:
                dists = [get_dist(dot.get_center(), c.get_center()) for c in centroids]
                closest_idx = np.argmin(dists)
                clusters[closest_idx].append(dot)
                assignment_anims.append(dot.animate.set_color(centroid_colors[closest_idx]))
            
            self.play(*assignment_anims, run_time=1)
            self.wait(0.5)

            # Update Step: Move centroids to the mean of their clusters
            move_anims = []
            for i, centroid in enumerate(centroids):
                if clusters[i]:
                    cluster_positions = [d.get_center() for d in clusters[i]]
                    mean_pos = np.mean(cluster_positions, axis=0)
                    move_anims.append(centroid.animate.move_to(mean_pos))
            
            self.play(*move_anims, run_time=1)
            self.wait(0.5)

        # 6. Final Cluster Centers as Discrete Targets
        final_targets = VGroup()
        for c in centroids:
            # Replace 'X' markers with solid dots to represent final quantization points
            t = Dot(c.get_center(), radius=0.18, color=c[0].get_color()).set_stroke(WHITE, 2)
            final_targets.add(t)
            
        self.play(
            ReplacementTransform(centroids, final_targets),
            data_points.animate.set_opacity(0.2)
        )
        
        # Concluding highlight
        self.play(
            *[Indicate(t, scale_factor=1.5) for t in final_targets]
        )
        self.wait(2)