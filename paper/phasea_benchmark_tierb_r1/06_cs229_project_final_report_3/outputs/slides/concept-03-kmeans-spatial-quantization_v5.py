from manim import *
import random
import numpy as np

class ConceptKMeansSpatialQuantization(Scene):
    def construct(self):
        # 1. Define the country outline (Simplified Australia-like polygon)
        aus_points = [
            [-3, 1.5, 0], [-1, 2, 0], [1, 1.8, 0], [3, 1.5, 0],
            [3.5, 0, 0], [2, -2, 0], [0, -2.5, 0], [-2, -2, 0],
            [-3.5, -0.5, 0], [-3, 1.5, 0]
        ]
        australia = Polygon(*aus_points, color=WHITE, fill_color=BLUE, fill_opacity=0.3)
        
        # 2. Place data points randomly
        data_dots = VGroup()
        random.seed(42)
        for _ in range(100):
            x = random.uniform(-3, 3)
            y = random.uniform(-2, 1.5)
            data_dots.add(Dot(point=[x, y, 0], radius=0.04, color=GRAY))

        # 3. Initial Centroids (Creating custom crosses since 'Cross' can be problematic)
        def create_cross(color):
            l1 = Line(UL, DR, stroke_width=4).scale(0.15)
            l2 = Line(UR, DL, stroke_width=4).scale(0.15)
            return VGroup(l1, l2).set_color(color)

        colors = [RED, GREEN, YELLOW, PURPLE]
        centroids = VGroup()
        for i in range(4):
            c = create_cross(colors[i])
            c.move_to([random.uniform(-2, 2), random.uniform(-1, 1), 0])
            centroids.add(c)

        # 4. Formula
        formula = MathTex(
            r"\mu_{j}:=\frac{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}x^{(i)}}{\sum_{i=1}^{n}\mathbf{1}\{c^{(i)}=j\}}"
        ).scale(0.8).to_edge(DOWN, buff=0.5)

        # 5. Narration Text
        narration = Text(
            "Turning regression into classification via spatial clustering.",
            font_size=24
        ).to_edge(UP, buff=0.5)

        # --- ANIMATION SEQUENCE ---

        # Intro
        self.play(Create(australia), Write(narration))
        self.play(FadeIn(data_dots, lag_ratio=0.02))
        self.wait(1)

        # Centroids appear
        self.play(AnimationGroup(*[Create(c) for c in centroids], lag_ratio=0.2))
        self.wait(1)

        # Assignment step: Points change color to nearest centroid
        assignment_anims = []
        for dot in data_dots:
            dists = [np.linalg.norm(dot.get_center() - c.get_center()) for c in centroids]
            nearest_idx = np.argmin(dists)
            assignment_anims.append(dot.animate.set_color(colors[nearest_idx]))
        
        self.play(*assignment_anims, run_time=2)
        self.wait(1)

        # Update step: Centroids move to mean of assigned points
        move_anims = []
        for i in range(len(centroids)):
            assigned_points = []
            for dot in data_dots:
                # Check color as a proxy for assignment
                if dot.get_color() == colors[i]:
                    assigned_points.append(dot.get_center())
            
            if assigned_points:
                new_pos = np.mean(assigned_points, axis=0)
                move_anims.append(centroids[i].animate.move_to(new_pos))
        
        self.play(Write(formula))
        self.play(*move_anims, run_time=2)
        self.wait(1)

        # Final highlight
        self.play(*[Indicate(c, color=WHITE) for c in centroids])
        self.wait(2)