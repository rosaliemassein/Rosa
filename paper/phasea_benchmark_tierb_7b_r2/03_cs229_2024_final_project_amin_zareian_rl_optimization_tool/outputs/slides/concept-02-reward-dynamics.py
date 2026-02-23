from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # Create a 3x3 grid
        grid = VGroup(*[VGroup(*[Square(side_length=1).set_fill(GRAY, opacity=0.8) for _ in range(3)]) for _ in range(3)])
        grid.arrange_in_grid(rows=3, cols=3)
        self.play(Create(grid), run_time=1.5)

        # Highlight the center pixel and its neighbors
        center_pixel = grid[1][1]
        neighbors = [grid[i][j] for i in range(2, 4) for j in range(2, 4)]
        
        # Animate the center pixel flipping from Red to Blue
        self.play(Transform(center_pixel, Square(side_length=1).set_fill(BLUE, opacity=0.8)), run_time=2)

        # Highlight new borders created
        highlight_green = Square(side_length=1).set_stroke(GREEN, width=2)
        self.play(Transform(neighbors[0], highlight_green), run_time=1)

        # Display a floating '+2' text next to the pixel
        reward_text = MathTex(r"+2").set_color(GREEN).scale(1.5)
        reward_text.next_to(center_pixel, RIGHT)
        self.play(FadeIn(reward_text), run_time=1)

        # Animate the center pixel flipping back to Red
        self.play(Transform(center_pixel, Square(side_length=1).set_fill(RED, opacity=0.8)), run_time=2)

        # Highlight borders lost
        self.play(Transform(neighbors[0], Square(side_length=1).set_fill(GRAY, opacity=0.8)), run_time=1)

        # Display a floating '-2' text next to the pixel
        reward_text_negative = MathTex(r"-2").set_color(RED).scale(1.5)
        reward_text_negative.next_to(center_pixel, RIGHT)
        self.play(FadeIn(reward_text_negative), run_time=1)

        # Clean up
        self.wait(2)