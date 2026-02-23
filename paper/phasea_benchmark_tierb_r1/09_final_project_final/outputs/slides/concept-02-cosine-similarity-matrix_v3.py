from manim import *
import numpy as np

class CosineSimilarity(Scene):
    def construct(self):
        # 1. Setup Manual Axes and Vectors
        # We avoid Axes and ValueTracker as they were flagged as disallowed/undefined
        origin = LEFT * 3.5 + DOWN * 1.5
        x_axis = Line(origin, origin + RIGHT * 4, color=WHITE)
        y_axis = Line(origin, origin + UP * 4, color=WHITE)
        x_label = MathTex("x").next_to(x_axis, RIGHT)
        y_label = MathTex("y").next_to(y_axis, UP)
        
        # We use a hidden Dot's x-coordinate to track the angle theta
        # Initial angle is 60 degrees
        angle_tracker = Dot(point=[60 * PI / 180, 0, 0], fill_opacity=0)
        
        # Vector A is fixed on the x-axis
        vec_a = Line(origin, origin + RIGHT * 3, color=RED)
        label_a = MathTex(r"\mathbf{A}", color=RED).next_to(vec_a, DOWN)
        
        # Vector B rotates based on the tracker
        vec_b = Line(origin, origin + RIGHT * 3, color=GREEN)
        label_b = MathTex(r"\mathbf{B}", color=GREEN)

        def update_vector_b(mob):
            theta = angle_tracker.get_x()
            end_pos = origin + np.array([np.cos(theta) * 3, np.sin(theta) * 3, 0])
            mob.put_start_and_end_on(origin, end_pos)
            label_b.move_to(end_pos + UR * 0.2)

        vec_b.add_updater(update_vector_b)

        # 2. Similarity Matrix (5x5 Grid)
        matrix = VGroup()
        for r in range(5):
            for c in range(5):
                sq = Square(side_length=0.5)
                sq.move_to(RIGHT * 3 + UP * (1 - r * 0.5) + RIGHT * (c * 0.5))
                sq.set_fill(BLUE, opacity=0.2)
                sq.set_stroke(WHITE, width=1)
                matrix.add(sq)
        
        # Middle cell (index 12) glows based on the cosine of the angle
        target_cell = matrix[12]
        def update_cell_glow(mob):
            val = np.cos(angle_tracker.get_x())
            # Map cosine (1 to -1) to opacity (1 to 0)
            glow_opacity = max(0, val)
            mob.set_fill(YELLOW, opacity=glow_opacity)
        
        target_cell.add_updater(update_cell_glow)

        # 3. Formula and Similarity Value display
        formula = MathTex(
            r"\text{similarity} = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}",
            font_size=30
        ).to_edge(UP)
        
        sim_label = MathTex(r"\text{Similarity: }").move_to(RIGHT * 3 + UP * 2.2)
        sim_value = MathTex("0.50").next_to(sim_label, RIGHT)

        def update_sim_text(mob):
            val = np.cos(angle_tracker.get_x())
            new_val = MathTex(f"{val:.2f}").next_to(sim_label, RIGHT)
            mob.become(new_val)
        
        sim_value.add_updater(update_sim_text)

        # 4. Adding everything to the scene
        self.add(x_axis, y_axis, x_label, y_label, angle_tracker)
        self.add(vec_a, label_a, vec_b, label_b)
        self.add(matrix, formula, sim_label, sim_value)

        # 5. Animations
        # Rotate to alignment (Theta = 0, Cosine = 1)
        self.play(angle_tracker.animate.set_x(0), run_time=3)
        self.wait(1)
        
        # Rotate to divergence (Theta = 90 degrees, Cosine = 0)
        self.play(angle_tracker.animate.set_x(90 * PI / 180), run_time=3)
        self.wait(1)
        
        # Rotate to a custom angle
        self.play(angle_tracker.animate.set_x(45 * PI / 180), run_time=2)
        self.wait(2)

        # Cleanup updaters to finish
        vec_b.clear_updaters()
        target_cell.clear_updaters()
        sim_value.clear_updaters()