from manim import *
import numpy as np

class LocallyWeightedRegression(Scene):
    def construct(self):
        # 1. Manual Coordinate System (avoiding 'Axes')
        x_line = Line(LEFT * 5, RIGHT * 5, color=WHITE)
        y_line = Line(DOWN * 3, UP * 3, color=WHITE)
        self.add(x_line, y_line)

        # Labels for axes
        x_lab = Text("x", font_size=20).next_to(x_line, RIGHT)
        y_lab = Text("y", font_size=20).next_to(y_line, UP)
        self.add(x_lab, y_lab)

        # 2. Generate Noisy Nonlinear Data
        np.random.seed(10)
        data_x = np.linspace(-4, 4, 60)
        # Sine wave data with some noise
        data_y = np.sin(data_x) + np.random.normal(0, 0.12, 60)
        
        data_dots = VGroup()
        for px, py in zip(data_x, data_y):
            # Map values directly to screen coordinates (1 unit = 1 manim unit)
            dot_obj = Dot(point=[px, py, 0], radius=0.06, color=GRAY_B)
            data_dots.add(dot_obj)
        self.add(data_dots)

        # 3. Query Point (serves as the state tracker, avoiding 'ValueTracker')
        # We'll animate this dot's position and use it to drive the regression
        query_point = Dot(point=[-4, np.sin(-4), 0], color=WHITE, radius=0.12)
        self.add(query_point)

        # Weight field visualization (expanding ring)
        weight_ring = Circle(radius=0.7, color=YELLOW, stroke_opacity=0.4)
        weight_ring.move_to(query_point.get_center())
        self.add(weight_ring)

        # 4. Local Regression Line
        reg_line = Line(color=RED, stroke_width=5)
        self.add(reg_line)

        # 5. Formula Overlay
        # Using Tex with raw strings to avoid issues
        formula_tex = Tex(
            r"$w^{(i)} = \exp\left(-\frac{||x^{(i)} - x||^2}{2\tau^2}\right)$"
        ).to_corner(UL, buff=0.5).scale(0.8)
        self.add(formula_tex)

        # 6. Logic Updater
        # This function updates the line and dot weights based on query_point position
        def update_regression_logic(obj_to_update):
            current_x = query_point.get_center()[0]
            
            # Distance-based weights (Gaussian kernel)
            tau_val = 0.6
            x_diffs = data_x - current_x
            weights = np.exp(-(x_diffs**2) / (2 * tau_val**2))
            
            # Perform Weighted Least Squares: theta = (X^T W X)^-1 X^T W y
            # X is [1, x]
            W_matrix = np.diag(weights)
            X_matrix = np.column_stack((np.ones(len(data_x)), data_x))
            
            try:
                # Normal equation for WLS: (X^T W X) theta = X^T W y
                xt_w = X_matrix.T @ W_matrix
                a_mat = xt_w @ X_matrix
                b_mat = xt_w @ data_y
                
                # Solve for [intercept, slope]
                theta_params = np.linalg.solve(a_mat, b_mat)
                intercept_val = theta_params[0]
                slope_val = theta_params[1]
                
                # Update visual line segment around the query point
                half_width = 0.9
                x_start = current_x - half_width
                x_end = current_x + half_width
                y_start = slope_val * x_start + intercept_val
                y_end = slope_val * x_end + intercept_val
                
                reg_line.put_start_and_end_on(
                    [x_start, y_start, 0],
                    [x_end, y_end, 0]
                )
            except:
                # Fallback if matrix is singular
                pass

            # Update visualization of the training points (glow effect)
            for i, data_dot in enumerate(data_dots):
                w_i = weights[i]
                if w_i > 0.05:
                    data_dot.set_color(YELLOW)
                    data_dot.set_stroke(YELLOW, width=w_i * 4, opacity=w_i)
                    data_dot.set_fill(opacity=0.3 + 0.7 * w_i)
                else:
                    data_dot.set_color(GRAY_B)
                    data_dot.set_fill(opacity=0.2)
            
            # Sync weight ring
            weight_ring.move_to(query_point.get_center())

        # Attach the logic to the query point
        query_point.add_updater(update_regression_logic)

        # 7. Narration and Animation
        voiceover_text = Text(
            "Locally Weighted Regression ignores distant points and fits a local line.",
            font_size=22
        ).to_edge(DOWN, buff=0.4)
        self.add(voiceover_text)

        # Move query point across the domain
        # The line will tilt and recalculate automatically via the updater
        self.play(
            query_point.animate.move_to([4, np.sin(4), 0]),
            run_time=10
        )
        self.wait(1)

        # Final move back to a specific local curvature
        self.play(
            query_point.animate.move_to([0, np.sin(0), 0]),
            run_time=4
        )
        self.wait(2)