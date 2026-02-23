from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # Create a 3x3 grid with numbers as pixels
        grid = VGroup(
            *[Square(color=RED) for i in range(9)],
            *[Square(color=BLUE) for _ in range(9)]
        ).arrange_in_grid(rows=3, cols=3).move_to([-1.5, 0])

        # Highlight the center pixel and its neighbors
        center_pixel = grid[4]
        neighbors = [grid[i] for i in range(8) if abs(i % 3 - 4) + abs(i // 3 - 4) == 1]
        center_pixel.set_color(RED).scale(1.2)
        for neighbor in neighbors:
            neighbor.set_color(GREEN)

        # Animate the center pixel flipping from Red to Blue
        self.play(
            Create(center_pixel),
            *[Transform(neighbor, BLUE) for neighbor in neighbors],
            run_time=2
        )

        # Highlight new borders created and 'X' marks for lost borders
        green_borders = VGroup(*[Square(color=GREEN) for _ in range(8)])
        red_x_marks = VGroup(*[Square(color=RED) for _ in range(8)])
        green_borders.arrange_in_grid(rows=2, cols=4).next_to(center_pixel, RIGHT)
        red_x_marks.arrange_in_grid(rows=2, cols=4).next_to(center_pixel, RIGHT)

        self.play(
            *[Transform(neighbor, GREEN) for i, neighbor in enumerate(neighbors)],
            Transform(center_pixel, BLUE),
            *[Transform(neighbor, RED) for i in range(4)],
            Transform(neighbors[0], RED),
            *[Transform(grid[j], BLUE) for j in range(9)],
            run_time=2
        )

        # Create a floating '+2' or '-2' text next to the pixel
        reward_text = Text("+2", color=GREEN, font_size=34).next_to(center_pixel, DOWN)
        self.play(
            Write(reward_text),
            run_time=2
        )

        # Show a floating '+2' or '-2' text next to the pixel
        reward_text = Text("-2", color=RED, font_size=34).next_to(center_pixel, DOWN)
        self.play(
            FadeIn(reward_text),
            run_time=2
        )

        # Link this to a BarChart showing the cumulative reward growing over time
        bar_chart = VGroup(
            *[Square(color=BLUE) for _ in range(10)],
            *[Square(color=RED) for _ in range(5)]
        ).arrange_in_grid(rows=2, cols=6).move_to([1.5, 0])
        self.play(
            Transform(reward_text, Text("+2", color=GREEN, font_size=34)).next_to(center_pixel, DOWN),
            Transform(bar_chart[0], BLUE),
            run_time=2
        )
        self.wait()