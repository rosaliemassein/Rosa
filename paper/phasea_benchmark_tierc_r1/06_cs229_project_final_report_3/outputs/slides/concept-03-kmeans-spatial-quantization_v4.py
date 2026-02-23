from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup the coordinate plane
        plane = NumberPlane(
            x_range=[0, 10, 1],
            y_range=[0, 6, 1],
            x_length=10,
            y_length=6,
            background_line_style={"stroke_opacity": 0.2}
        ).scale(0.8).to_edge(DOWN)
        
        # 2. Simple country-like shape (Australia-ish)
        country_coords = [
            [2, 4, 0], [4, 5, 0], [7, 4.5, 0], 
            [8, 3, 0], [7.5, 1.5, 0], [5, 1, 0], 
            [2, 1.5, 0], [1.5, 3, 0]
        ]
        australia_pts = [plane.c2p(*p) for p in country_coords]
        country_outline = Polygon(*australia_pts, color=WHITE, stroke_width=2, fill_opacity=0.1)
        
        # 3. Generate random training points within a bounding box for safety
        np.random.seed(15)
        points_list = []
        while len(points_list) < 120:
            # Generate points roughly in the center area
            p_rand = [np.random.uniform(2, 7.5), np.random.uniform(1.5, 4.5), 0]
            points_list.append(plane.c2p(*p_rand))
        
        dots = VGroup(*[Dot(p, radius=0.04, color=GRAY) for p in points_list])
        
        # 4. Text and Formula
        voice_text = Text(
            "Simplifying continuous coordinates via spatial clustering.",
            font_size=24
        ).to_edge(UP, buff=0.3)
        
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            font_size=32
        ).next_to(voice_text, DOWN, buff=0.2)
        
        self.play(Create(plane), Create(country_outline))
        self.play(FadeIn(dots), Write(voice_text))
        self.wait(1)
        
        # 5. Initialize Centroids (Manual Cross markers)
        K = 5
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        # Defined initial starting points for centroids
        start_centers_raw = [[3, 4, 0], [6, 2, 0], [2.5, 2.5, 0], [7, 4, 0], [4.5, 3, 0]]
        start_centers = [plane.c2p(*p) for p in start_centers_raw]
        
        def get_centroid_marker(color):
            # Create a cross manually using two lines
            l1 = Line(0.15 * UL, 0.15 * DR, color=color, stroke_width=5)
            l2 = Line(0.15 * UR, 0.15 * DL, color=color, stroke_width=5)
            c = Circle(radius=0.2, color=color, stroke_opacity=0.4)
            return VGroup(l1, l2, c)

        centroids = VGroup(*[
            get_centroid_marker(colors[i]).move_to(start_centers[i])
            for i in range(K)
        ])
        
        self.play(FadeIn(centroids, shift=UP), Write(formula))
        self.wait(1)
        
        # 6. K-Means Assignment Step: Change dot colors based on nearest centroid
        centroid_positions = [c.get_center() for c in centroids]
        assignments = []
        for dot in dots:
            distances = [np.linalg.norm(dot.get_center() - cp) for cp in centroid_positions]
            assignments.append(np.argmin(distances))
        
        self.play(*[
            dots[i].animate.set_color(colors[assignments[i]])
            for i in range(len(dots))
        ], run_time=2)
        self.wait(1)
        
        # 7. K-Means Update Step: Move centroids to the center of their colored groups
        move_anims = []
        for k in range(K):
            assigned_points = [
                dots[i].get_center() 
                for i, cluster_idx in enumerate(assignments) 
                if cluster_idx == k
            ]
            if assigned_points:
                new_mean = np.mean(assigned_points, axis=0)
                move_anims.append(centroids[k].animate.move_to(new_mean))
        
        self.play(*move_anims, run_time=2)
        self.wait(1)
        
        # 8. Final Goal/Conclusion
        goal_text = Text(
            "Discretized space into predictable classification regions.", 
            font_size=24, color=YELLOW
        ).to_edge(UP)
        
        self.play(FadeOut(voice_text), FadeIn(goal_text))
        self.play(
            centroids.animate.scale(1.2),
            dots.animate.set_opacity(0.3)
        )
        self.wait(2)