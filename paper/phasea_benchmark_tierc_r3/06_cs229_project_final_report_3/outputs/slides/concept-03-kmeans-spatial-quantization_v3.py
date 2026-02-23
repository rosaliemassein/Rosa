from manim import *
import numpy as np

class Concept03KMeansSpatialQuantization(Scene):
    def construct(self):
        # 1. Setup Plane and Australia-like Shape
        plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            background_line_style={"stroke_opacity": 0.4}
        )
        
        australia_points = [
            [-3, 1.5, 0], [-1, 2, 0], [1.5, 1.8, 0], [3.5, 1, 0], 
            [4, -1, 0], [3, -2.5, 0], [1, -2.2, 0], [-1.5, -3, 0], 
            [-3.5, -2, 0], [-4, 0, 0]
        ]
        australia = Polygon(*australia_points, color=WHITE, stroke_width=2, fill_opacity=0.1)
        
        self.add(plane)
        self.play(Create(australia))
        self.wait(0.5)

        # 2. Populate with Gray Dots (Data Points)
        np.random.seed(42)
        dots_coords = []
        for _ in range(60):
            x = np.random.uniform(-3.5, 3.5)
            y = np.random.uniform(-2.5, 1.5)
            dots_coords.append(np.array([x, y, 0]))
            
        dots = VGroup(*[Dot(point=c, radius=0.08, color=GRAY) for c in dots_coords])
        self.play(FadeIn(dots, shift=UP))
        self.wait(0.5)

        # 3. Add Centroids (mu_j) using Lines for crosses
        colors = [RED, BLUE, GREEN]
        centroid_positions = [
            np.array([-2.5, 0.5, 0]),
            np.array([0.5, 1.2, 0]),
            np.array([2.0, -1.5, 0])
        ]
        
        def create_cross(pos, color):
            l1 = Line(UL, DR, stroke_width=4).scale(0.15).move_to(pos).set_color(color)
            l2 = Line(UR, DL, stroke_width=4).scale(0.15).move_to(pos).set_color(color)
            return VGroup(l1, l2)

        centroids = VGroup(*[
            create_cross(pos, colors[i])
            for i, pos in enumerate(centroid_positions)
        ])
        
        centroid_labels = VGroup(*[
            MathTex(rf"\mu_{i+1}", font_size=24, color=colors[i]).next_to(centroids[i], UR, buff=0.05)
            for i in range(len(centroids))
        ])

        self.play(
            *[Create(c) for c in centroids],
            *[Write(l) for l in centroid_labels]
        )
        self.wait(1)

        # 4. K-Means Iteration Logic
        def get_assignments(dot_positions, c_positions):
            assignments = []
            for dp in dot_positions:
                distances = [np.linalg.norm(dp - cp) for cp in c_positions]
                assignments.append(np.argmin(distances))
            return assignments

        # Initial assignment and coloring
        dot_positions = [d.get_center() for d in dots]
        current_centroid_pos = [c.get_center() for c in centroids]
        assignments = get_assignments(dot_positions, current_centroid_pos)
        
        self.play(*[
            dots[i].animate.set_color(colors[assignments[i]])
            for i in range(len(dots))
        ])
        self.wait(0.5)

        # Iterations
        for _ in range(2):
            # Calculate new means
            new_positions = []
            for j in range(len(centroids)):
                assigned_to_j = [dot_positions[i] for i, a in enumerate(assignments) if a == j]
                if assigned_to_j:
                    new_positions.append(np.mean(assigned_to_j, axis=0))
                else:
                    new_positions.append(current_centroid_pos[j])

            # Animate movement
            move_anims = []
            for j in range(len(centroids)):
                move_anims.append(centroids[j].animate.move_to(new_positions[j]))
                move_anims.append(centroid_labels[j].animate.next_to(new_positions[j], UR, buff=0.05))
            
            self.play(*move_anims)
            current_centroid_pos = new_positions
            
            # Re-assign and re-color
            assignments = get_assignments(dot_positions, current_centroid_pos)
            self.play(*[
                dots[i].animate.set_color(colors[assignments[i]])
                for i in range(len(dots))
            ])
            self.wait(0.5)

        # 5. Formula and Final Highlights
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}",
            font_size=36
        ).to_edge(UP).add_background_rectangle()
        
        final_targets = VGroup(*[
            Circle(radius=0.3, color=colors[i], stroke_width=3).move_to(centroids[i].get_center())
            for i in range(len(centroids))
        ])

        self.play(Write(formula))
        self.play(Create(final_targets))
        self.wait(2)