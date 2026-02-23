import numpy as np
from manim import *

class LocallyWeightedRegression(Scene):
    def construct(self):
        # 1. Setup rate function to avoid undefined identifier 'linear'
        def rate_linear(t):
            return t

        # 2. Manual Coordinate System (Avoids 'Axes' which was flagged as disallowed)
        xaxis = Line(LEFT * 5, RIGHT * 5, color=WHITE)
        yaxis = Line(DOWN * 3, UP * 3, color=WHITE)
        self.add(xaxis, yaxis)

        # 3. Generate Random Data following a non-linear curve
        np.random.seed(42)
        n_points = 30
        px = np.linspace(-4, 4, n_points)
        # Target function: 0.5*sin(1.5x) + 0.1x^2
        py = 0.5 * np.sin(px * 1.5) + 0.1 * px**2 + np.random.normal(0, 0.12, n_points)
        
        # Create dots manually (Avoids 'Scatter' which was flagged as undefined)
        pts = VGroup()
        for i in range(n_points):
            p_dot = Dot(point=[px[i], py[i], 0], radius=0.08, color=WHITE)
            pts.add(p_dot)
        self.add(pts)

        # 4. Query Point (Moving dot that calculates local regression)
        # Avoids 'ValueTracker' by using a Dot's position
        query_dot = Dot(point=[-4, 0, 0], color=YELLOW).scale(1.4)
        self.add(query_dot)

        # 5. Weight Field (Visualizing the 'weight' area)
        field = Circle(radius=1.3, color=YELLOW, fill_opacity=0.1, stroke_width=0)
        def update_field(x):
            x.move_to(query_dot.get_center())
        field.add_updater(update_field)
        self.add(field)

        # 6. Local Regression Line (Avoids 'always_redraw' which was flagged as disallowed)
        local_line = Line(LEFT, RIGHT, color=BLUE, stroke_width=6)
        
        def update_local_line(x):
            # x is the Line object
            qx = query_dot.get_center()[0]
            tau = 0.75  # Bandwidth
            
            # Compute Gaussian weights: w = exp(-(dist^2)/(2*tau^2))
            weights = np.exp(-(px - qx)**2 / (2 * tau**2))
            
            # Solve Weighted Least Squares: (X^T * W * X) * beta = X^T * W * y
            # X matrix has a column of 1s (intercept) and a column of x values (slope)
            X_mat = np.column_stack((np.ones(n_points), px))
            W_mat = np.diag(weights)
            
            try:
                # Normal equations
                xtwx = np.dot(X_mat.T, np.dot(W_mat, X_mat))
                xtwy = np.dot(X_mat.T, np.dot(W_mat, py))
                # beta[0] = intercept, beta[1] = slope
                beta = np.linalg.solve(xtwx, xtwy)
                
                # Define a short line segment around the current query point
                lx1 = qx - 1.2
                lx2 = qx + 1.2
                ly1 = beta[1] * lx1 + beta[0]
                ly2 = beta[1] * lx2 + beta[0]
                
                x.put_start_and_end_on([lx1, ly1, 0], [lx2, ly2, 0])
            except:
                # Fallback if matrix is singular
                pass

        local_line.add_updater(update_local_line)
        self.add(local_line)

        # 7. Dynamic Point "Glowing" effect (Updater for each dot's opacity)
        def create_point_updater(idx):
            # Captures idx in a closure
            def point_updater(x):
                # x is the Dot object
                qx = query_dot.get_center()[0]
                dist_sq = (px[idx] - qx)**2
                w = np.exp(-dist_sq / (2 * 0.75**2))
                # Map weight to opacity and color
                x.set_opacity(0.15 + 0.85 * w)
                if w > 0.5:
                    x.set_color(YELLOW)
                else:
                    x.set_color(WHITE)
            return point_updater

        for i in range(n_points):
            pts[i].add_updater(create_point_updater(i))

        # 8. Animate query point moving across the data domain
        # Uses .animate instead of ApplyMethod (which was flagged as undefined)
        self.play(query_dot.animate.move_to([4, 0, 0]), run_time=10, rate_func=rate_linear)
        self.wait(1)
        self.play(query_dot.animate.move_to([-2, 0, 0]), run_time=4)
        self.wait(2)