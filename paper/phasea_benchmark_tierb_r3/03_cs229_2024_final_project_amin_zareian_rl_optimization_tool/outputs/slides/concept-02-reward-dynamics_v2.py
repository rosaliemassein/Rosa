from manim import *

class Concept02RewardDynamics(Scene):
    def construct(self):
        # Create a 3x3 grid
        square = Square(color=WHITE, fill_color=YELLOW, fill_opacity=0.4)
        grid = VGroup(*[square for _ in range(9)]).arrange_in_grid(rows=3, cols=3)

        # Place the grid
        self.play(Create(grid), run_time=1)
        self.wait()

        # Define the center pixel and its neighbors
        center_pixel = grid[4].copy().scale(1.5)
        neighbors = [grid[i] for i in [0, 2, 6, 8]]

        # Animate the center pixel flipping from Red to Blue
        border_colors = {'Red': BLUE, 'Blue': RED}
        for color in ['Red', 'Blue']:
            self.play(Transform(center_pixel, center_pixel.copy().set_color(border_colors[color])))
            border_length = len({xy for xy in neighbors if grid[xy].color == color})
            self.wait(0.5)

        # Highlight new borders created and red 'X' marks for borders lost
        new_borders = {xy for xy in neighbors if grid[xy].color == center_pixel.color}
        self.play(FadeIn(grid[grid.index(min((x, y) for x, y in new_borders.items()))], scale=1.2))
        self.play(FadeIn(grid[grid.index(max((x, y) for x, y in new_borders.items()))], scale=1.2))
        self.wait(0.5)
        for xy in new_borders:
            if center_pixel.color == grid[xy].color:
                self.play(FadeOut(grid[xy]), run_time=0.2)
            else:
                self.play(Indicate(grid[xy]), run_time=0.3)

        # Display a floating '+2' or '-2' text next to the pixel based on the net change in border length
        net_change = [new_borders].count(center_pixel) - neighbors.count(center_pixel)
        text = Text(f"+{net_change}", color=RED).scale(0.5).next_to(center_pixel, RIGHT)
        self.play(Create(text), run_time=1)

        # Link this to a BarChart showing the cumulative reward growing over time
        bar_chart = VGroup(*(Text(f"+{i+1}", color=RED) for i in range(6))).arrange_in_grid(rows=2, cols=3).next_to(center_pixel, DOWN)
        self.play(Create(bar_chart), run_time=1)

        # Narration
        self.wait(2)