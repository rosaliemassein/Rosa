from manim import *

class BorderOptimization(Scene):
    def construct(self):
        # Create a 4x4 grid of squares
        grid = VGroup(*[Square() for _ in range(16)]).arrange_in_grid(rows=4, cols=4)
        grid.shift(RIGHT * 2)

        # Color the left half red and the right half blue
        for i in range(4):
            grid[i].set_fill(color=RED, opacity=1)
        for i in range(4, 8):
            grid[i].set_fill(color=BLUE, opacity=1)

        # Draw green lines between adjacent pixels
        border_lines = VGroup()
        for i in range(16):
            if (i % 4 != 3):
                border_lines += Line(grid[i].get_bottom(), grid[i + 1].get_top()).set_color(GREEN)
            if (i < 12):
                border_lines += Line(grid[i].get_right(), grid[i + 4].get_left()).set_color(GREEN)

        # Add the grid and border lines to the scene
        self.play(Create(grid), Create(border_lines))
        self.wait()

        # Animation for flipping colors to checkerboard pattern
        counter = MathTex(r"B = 0").set_color(BLACK).scale(1.5)
        counter.to_corner(UL)
        self.play(Create(counter))

        for i in range(16):
            if (i % 2 == 0 and i // 4 % 2 == 0) or (i % 2 != 0 and i // 4 % 2 != 0):
                self.play(Transform(grid[i], Square().set_fill(color=BLUE, opacity=1)))
            else:
                self.play(Transform(grid[i], Square().set_fill(color=RED, opacity=1)))
            border_lines = VGroup()
            for j in range(16):
                if (j % 4 != 3):
                    border_lines += Line(grid[j].get_bottom(), grid[j + 1].get_top()).set_color(GREEN)
                if (j < 12):
                    border_lines += Line(grid[j].get_right(), grid[j + 4].get_left()).set_color(GREEN)
            self.play(Transform(border_lines, border_lines))
            if (i % 2 == 0 and i // 4 % 2 == 0) or (i % 2 != 0 and i // 4 % 2 != 0):
                self.play(counter.animate.shift(RIGHT * 1.5), run_time=0.3)
            else:
                self.play(counter.animate.shift(LEFT * 1.5), run_time=0.3)
        self.wait()