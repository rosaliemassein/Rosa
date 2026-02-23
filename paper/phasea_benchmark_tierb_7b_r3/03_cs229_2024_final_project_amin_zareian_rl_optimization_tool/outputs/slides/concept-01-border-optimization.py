from manim import *

class BorderOptimization(Scene):
    def construct(self):
        # Create a 4x4 grid of squares
        squares = VGroup(*[Square() for _ in range(16)]).arrange_in_grid(rows=4, columns=4)
        squares.shift(RIGHT * 2)

        # Color the left half red and right half blue
        for i in range(16):
            if i < 8:
                squares[i].set_fill(RED, opacity=1)
            else:
                squares[i].set_fill(BLUE, opacity=1)

        # Draw thick green lines between adjacent pixels of different colors
        borders = VGroup()
        for i in range(16):
            if squares[i].get_color() != squares[(i + 1) % 4].get_color():
                borders.add(Line(squares[i].get_right(), squares[(i + 1) % 4].get_left()).set_stroke(BLUE, 2))
            if squares[i].get_color() != squares[(i + 4) % 16].get_color():
                borders.add(Line(squares[i].get_bottom(), squares[(i + 4) % 16].get_top()).set_stroke(BLUE, 2))

        # Add squares and borders to the scene
        self.add(squares, borders)

        # Create a counter for border length
        counter = MathTex(r"B = 0", color=WHITE).to_corner(UL).scale(1.5)

        # Animate the squares flipping colors to checkerboard pattern
        for i in range(16):
            if (i // 4) % 2 == 0:
                squares[i].set_color(BLUE if i % 2 == 0 else RED)
            else:
                squares[i].set_color(RED if i % 2 == 0 else BLUE)
            self.play(Transform(squares[i], squares[i].copy().set_color(BLUE if i % 2 == 0 else RED)), run_time=0.1)
            for border in borders:
                if squares[i].get_color() != squares[(i + 1) % 4].get_color():
                    border.set_color(BLUE)
                else:
                    border.set_color(WHITE)
                if squares[i].get_color() != squares[(i + 4) % 16].get_color():
                    border.set_color(BLUE)
                else:
                    border.set_color(WHITE)
            self.play(Transform(counter, MathTex(r"B = " + str(i + 1), color=WHITE).to_corner(UL).scale(1.5)), run_time=0.1)

        # Display final border count
        self.wait(2)