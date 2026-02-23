from manim import *
import numpy as np

class BorderOptimization(Scene):
    def construct(self):
        # 1. UI Setup
        formula = MathTex(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]").to_edge(UP, buff=0.7)
        title = Text("Border Length Optimization", font_size=32).next_to(formula, UP, buff=0.2)
        
        # 4x4 Grid
        grid = VGroup(*[
            Square(side_length=0.8, fill_opacity=1, stroke_width=2, stroke_color=WHITE)
            for _ in range(16)
        ]).arrange_in_grid(4, 4, buff=0.2).shift(LEFT * 1.5)

        # Initial state: Left half red (cols 0,1), right half blue (cols 2,3)
        for i in range(16):
            col = i % 4
            if col < 2:
                grid[i].set_fill(RED)
            else:
                grid[i].set_fill(BLUE)

        # 2. Border Line Logic
        def get_border_mobjects(grid_group):
            lines = VGroup()
            count = 0
            for idx in range(16):
                r, c = idx // 4, idx % 4
                # Right neighbor
                if c < 3:
                    if not np.array_equal(grid_group[idx].get_fill_color(), grid_group[idx+1].get_fill_color()):
                        p1 = grid_group[idx].get_right()
                        p2 = grid_group[idx+1].get_left()
                        mid = (p1 + p2) / 2
                        lines.add(Line(mid + UP*0.4, mid + DOWN*0.4, color=GREEN, stroke_width=8))
                        count += 1
                # Bottom neighbor
                if r < 3:
                    if not np.array_equal(grid_group[idx].get_fill_color(), grid_group[idx+4].get_fill_color()):
                        p1 = grid_group[idx].get_bottom()
                        p2 = grid_group[idx+4].get_top()
                        mid = (p1 + p2) / 2
                        lines.add(Line(mid + LEFT*0.4, mid + RIGHT*0.4, color=GREEN, stroke_width=8))
                        count += 1
            return lines, count

        # 3. Initial Display
        current_lines, current_count = get_border_mobjects(grid)
        
        counter_label = Text("Border Length (B):", font_size=28)
        counter_val = Text(str(current_count), font_size=48, color=GREEN)
        counter_group = VGroup(counter_label, counter_val).arrange(DOWN, buff=0.3).next_to(grid, RIGHT, buff=1.2)
        
        self.add(title, formula, grid, current_lines, counter_group)
        self.wait(1)

        # 4. Step-by-step Transformation to Checkerboard
        # Pattern: (row + col) % 2 == 0 -> RED, else BLUE
        for i in range(16):
            r, c = i // 4, i % 4
            target_is_red = (r + c) % 2 == 0
            current_is_red = (c < 2) # based on initial setup logic
            
            # If color needs to change
            if target_is_red != current_is_red:
                new_color = RED if target_is_red else BLUE
                
                # We "manually" update the grid color for calculation
                grid[i].set_fill(new_color)
                
                # Generate new border lines and count
                next_lines, next_count = get_border_mobjects(grid)
                next_counter_val = Text(str(next_count), font_size=48, color=GREEN).move_to(counter_val)
                
                # Reset color for animation start
                grid[i].set_fill(RED if current_is_red else BLUE)
                
                # Play update animation
                self.play(
                    grid[i].animate.set_fill(new_color).rotate(PI, axis=RIGHT),
                    ReplacementTransform(current_lines, next_lines),
                    ReplacementTransform(counter_val, next_counter_val),
                    run_time=0.3
                )
                
                # Update tracking references
                current_lines = next_lines
                counter_val = next_counter_val
                # Update our logical state for the next check
                # (handled by the fact that grid[i] color is now changed)

        self.wait(2)