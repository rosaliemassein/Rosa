from manim import *
import numpy as np

class Concept01BorderOptimization(Scene):
    def construct(self):
        # 1. Setup the 4x4 Grid
        N = 4
        square_size = 0.8
        buff = 0.1
        squares = VGroup()
        
        # Initial state: Left half RED (cols 0, 1), Right half BLUE (cols 2, 3)
        for r in range(N):
            for c in range(N):
                initial_color = RED if c < 2 else BLUE
                sq = Square(
                    side_length=square_size, 
                    fill_opacity=1, 
                    fill_color=initial_color, 
                    stroke_color=WHITE, 
                    stroke_width=2
                )
                squares.add(sq)
        
        squares.arrange_in_grid(N, N, buff=buff).shift(LEFT * 2)

        # 2. Border and Counter logic functions
        # This function scans the grid to find adjacencies with different colors
        def get_current_adjacencies():
            lines = VGroup()
            count = 0
            for r in range(N):
                for c in range(N):
                    idx = r * N + c
                    curr_sq = squares[idx]
                    
                    # Check Right neighbor
                    if c < N - 1:
                        right_sq = squares[idx + 1]
                        if not np.array_equal(curr_sq.get_fill_color(), right_sq.get_fill_color()):
                            count += 1
                            p1 = (curr_sq.get_corner(UR) + curr_sq.get_corner(DR)) / 2
                            p2 = (right_sq.get_corner(UL) + right_sq.get_corner(DL)) / 2
                            mid = (p1 + p2) / 2
                            lines.add(Line(mid + UP*0.35, mid + DOWN*0.35, color=GREEN, stroke_width=10))
                    
                    # Check Down neighbor
                    if r < N - 1:
                        down_sq = squares[idx + N]
                        if not np.array_equal(curr_sq.get_fill_color(), down_sq.get_fill_color()):
                            count += 1
                            p1 = (curr_sq.get_corner(DL) + curr_sq.get_corner(DR)) / 2
                            p2 = (down_sq.get_corner(UL) + down_sq.get_corner(UR)) / 2
                            mid = (p1 + p2) / 2
                            lines.add(Line(mid + LEFT*0.35, mid + RIGHT*0.35, color=GREEN, stroke_width=10))
            return lines, count

        # 3. Dynamic UI elements using updaters/redrawers
        border_lines = always_redraw(lambda: get_current_adjacencies()[0])
        
        formula = MathTex(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]").scale(0.8).to_edge(UP)
        
        counter_label = MathTex("B = ").scale(1.2).shift(RIGHT * 3.5 + UP * 0.5)
        # Using DecimalNumber with 0 decimal places to replace Integer for environment compatibility
        counter_val = always_redraw(lambda: DecimalNumber(
            float(get_current_adjacencies()[1]), 
            num_decimal_places=0
        ).scale(1.2).next_to(counter_label, RIGHT))

        objective_text = Text("Maximize Border Adjacency", font_size=24).next_to(formula, DOWN)

        self.add(squares, border_lines, formula, counter_label, counter_val, objective_text)
        self.wait(1)

        # 4. Animation: Convert to Checkerboard pattern one pixel at a time
        # Target: (r + c) % 2 == 0 -> RED, else BLUE
        for r in range(N):
            for c in range(N):
                idx = r * N + c
                target_color = RED if (r + c) % 2 == 0 else BLUE
                # Only animate if the color needs to change
                if not np.array_equal(squares[idx].get_fill_color(), target_color):
                    self.play(
                        squares[idx].animate.set_fill(target_color),
                        run_time=0.3
                    )

        # 5. Final message showing the checkerboard is the optimal state
        final_text = Text("Maximized State: Checkerboard", font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)