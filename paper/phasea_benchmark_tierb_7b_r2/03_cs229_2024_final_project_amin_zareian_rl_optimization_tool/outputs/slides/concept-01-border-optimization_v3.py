from manim import *

class BorderOptimization(Scene):
    def construct(self):
        # Create a 4x4 grid of Square objects
        squares = VGroup(*[
            Square(side_length=0.8, fill_opacity=1, stroke_color=WHITE, stroke_width=1) 
            for _ in range(16)
        ])
        squares.arrange_in_grid(rows=4, columns=4, buff=0.1)
        squares.move_to(ORIGIN)

        # Initial coloring: left half red, right half blue
        # col 0, 1 -> RED; col 2, 3 -> BLUE
        current_colors = []
        for i in range(16):
            col = i % 4
            c = RED if col < 2 else BLUE
            squares[i].set_fill(c)
            current_colors.append(c)
        
        # Helper function to generate border lines based on current colors
        def get_lines(colors, sq_group):
            lines = VGroup()
            for i in range(16):
                r, c = i // 4, i % 4
                # Check right neighbor for color difference
                if c < 3:
                    if colors[i] != colors[i+1]:
                        mid = (sq_group[i].get_center() + sq_group[i+1].get_center()) / 2
                        lines.add(Line(mid + UP * 0.4, mid + DOWN * 0.4, color=GREEN, stroke_width=6))
                # Check bottom neighbor for color difference
                if r < 3:
                    if colors[i] != colors[i+4]:
                        mid = (sq_group[i].get_center() + sq_group[i+4].get_center()) / 2
                        lines.add(Line(mid + LEFT * 0.4, mid + RIGHT * 0.4, color=GREEN, stroke_width=6))
            return lines

        # Helper function to calculate total adjacency score
        def get_score(colors):
            s = 0
            for i in range(16):
                r, c = i // 4, i % 4
                if c < 3 and colors[i] != colors[i+1]: s += 1
                if r < 3 and colors[i] != colors[i+4]: s += 1
            return s

        # Create initial borders and text elements
        borders = get_lines(current_colors, squares)
        score = get_score(current_colors)
        counter = MathTex("B = " + str(score)).to_corner(UR, buff=1)
        formula = MathTex(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]").to_edge(UP, buff=0.5)

        # Add initial objects to scene
        self.add(squares, borders, counter, formula)
        self.wait(1)

        # Animation: Flip pixels one by one to achieve a checkerboard pattern
        # This pattern maximizes the border length (B)
        for i in range(16):
            r, c = i // 4, i % 4
            # Target color for checkerboard: (row + col) is even -> RED, else BLUE
            target = RED if (r + c) % 2 == 0 else BLUE
            
            if current_colors[i] != target:
                # Update state
                current_colors[i] = target
                
                # Prepare updated visual states for Transform
                new_borders = get_lines(current_colors, squares)
                new_score = get_score(current_colors)
                new_counter = MathTex("B = " + str(new_score)).move_to(counter)
                
                # Animate the transition for the pixel, the borders, and the counter
                self.play(
                    squares[i].animate.set_fill(target),
                    Transform(borders, new_borders),
                    Transform(counter, new_counter),
                    run_time=0.3
                )
        
        self.wait(2)