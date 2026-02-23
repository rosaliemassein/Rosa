from manim import *

class BorderOptimization(Scene):
    def construct(self):
        grid_size = 4
        square_side_length = 1
        border_thickness = 0.2
        counter_text = Text("B = 3", font_size=24).to_edge(UL)

        squares = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                square = Square(side_length=square_side_length, color=RED if (i + j) % 2 == 0 else BLUE).move_to([i * square_side_length, j * square_side_length, 0])
                squares.add(square)
        self.play(Create(squares))

        border_lines = VGroup()
        for i in range(grid_size):
            for j in range(grid_size - 1):
                if (i + j) % 2 == 0:
                    border_line = Line([i * square_side_length, j * square_side_length, 0], [(i + 1) * square_side_length, j * square_side_length, 0], color=GREEN)
                else:
                    border_line = Line([i * square_side_length, j * square_side_length + 0.5 * border_thickness, 0], [(i + 1) * square_side_length, j * square_side_length + 0.5 * border_thickness, 0], color=GREEN)
                border_lines.add(border_line)

        for j in range(grid_size):
            for i in range(grid_size - 1):
                if (i + j) % 2 == 0:
                    border_line = Line([i * square_side_length, j * square_side_length, 0], [i * square_side_length, (j + 1) * square_side_length, 0], color=GREEN)
                else:
                    border_line = Line([i * square_side_length + 0.5 * border_thickness, j * square_side_length, 0], [i * square_side_length + 0.5 * border_thickness, (j + 1) * square_side_length, 0], color=GREEN)
                border_lines.add(border_line)

        self.play(Create(border_lines))

        def flip_color(square, target_color):
            new_square = square.copy().set_color(target_color)
            return Transform(square, new_square)

        counter_value = 3
        for i in range(grid_size):
            for j in range(grid_size):
                if (i + j) % 2 != 0:
                    self.play(flip_color(squares[i * grid_size + j], BLUE), run_time=0.5)
                    counter_value += 1
        counter_text.become(Text(f"B = {counter_value}", font_size=24).to_edge(UL))

        for i in range(grid_size):
            for j in range(grid_size):
                if (i + j) % 2 == 0:
                    self.play(flip_color(squares[i * grid_size + j], RED), run_time=0.5)
                    counter_value += 1
        counter_text.become(Text(f"B = {counter_value}", font_size=24).to_edge(UL))

        self.wait()