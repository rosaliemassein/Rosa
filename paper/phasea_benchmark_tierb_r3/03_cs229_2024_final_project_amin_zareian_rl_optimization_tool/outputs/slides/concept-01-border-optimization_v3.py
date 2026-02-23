from manim import *

class BorderOptimization(Scene):
    def construct(self):
        # 1. Title and Objective
        title = Text("Border Optimization", font_size=36).to_edge(UP)
        formula = MathTex(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]", font_size=32).next_to(title, DOWN)
        self.add(title, formula)

        # 2. Create 4x4 Grid of Squares
        squares = VGroup()
        for i in range(16):
            sq = Square(side_length=0.7, fill_opacity=1, stroke_width=2, stroke_color=WHITE)
            col = i % 4
            if col < 2:
                sq.set_fill(RED)
            else:
                sq.set_fill(BLUE)
            squares.add(sq)
        
        squares.arrange_in_grid(4, 4, buff=0.1).shift(LEFT * 1.5 + DOWN * 0.5)
        self.add(squares)

        # 3. Helper Function to Generate Border Lines
        def get_borders(sq_group):
            lines = VGroup()
            for i in range(16):
                r, c = i // 4, i % 4
                # Check Right neighbor
                if c < 3:
                    # Compare fill colors
                    if sq_group[i].get_fill_color() != sq_group[i+1].get_fill_color():
                        mid_point = (sq_group[i].get_center() + sq_group[i+1].get_center()) / 2
                        lines.add(Line(
                            mid_point + UP * 0.35, 
                            mid_point + DOWN * 0.35, 
                            color=GREEN, 
                            stroke_width=8
                        ))
                # Check Bottom neighbor
                if r < 3:
                    # Compare fill colors
                    if sq_group[i].get_fill_color() != sq_group[i+4].get_fill_color():
                        mid_point = (sq_group[i].get_center() + sq_group[i+4].get_center()) / 2
                        lines.add(Line(
                            mid_point + LEFT * 0.35, 
                            mid_point + RIGHT * 0.35, 
                            color=GREEN, 
                            stroke_width=8
                        ))
            return lines

        # 4. Initial Border Visuals and Counter
        current_borders = get_borders(squares)
        self.add(current_borders)

        counter_label = Text("Adjacencies:", font_size=24).to_edge(RIGHT, buff=1.5).shift(UP)
        count_val = MathTex(str(len(current_borders)), font_size=48, color=GREEN).next_to(counter_label, DOWN)
        self.add(counter_label, count_val)

        # 5. Determine flipping order to achieve Checkerboard
        # Checkerboard target: (row + col) % 2 == 0 -> RED, else BLUE
        flip_indices = []
        for i in range(16):
            r, c = i // 4, i % 4
            target_is_red = ((r + c) % 2 == 0)
            # Initial state: col < 2 is Red
            initial_is_red = (c < 2)
            if target_is_red != initial_is_red:
                flip_indices.append(i)

        self.wait(1)

        # 6. Animation Loop
        for idx in flip_indices:
            r, c = idx // 4, idx % 4
            target_color = RED if (r + c) % 2 == 0 else BLUE
            
            # Update internal state to calculate new geometry
            old_color = squares[idx].get_fill_color()
            squares[idx].set_fill(target_color)
            new_border_group = get_borders(squares)
            new_count = len(new_border_group)
            
            # Prepare UI update
            new_count_val = MathTex(str(new_count), font_size=48, color=GREEN).move_to(count_val)
            
            # Reset square to old color for the animation step
            squares[idx].set_fill(old_color)
            
            # Play combined animation
            self.play(
                squares[idx].animate.set_fill(target_color),
                current_borders.animate.become(new_border_group),
                count_val.animate.become(new_count_val),
                run_time=0.4
            )

        self.wait(2)