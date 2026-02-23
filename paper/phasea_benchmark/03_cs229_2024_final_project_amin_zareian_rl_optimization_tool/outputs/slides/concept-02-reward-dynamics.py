from manim import *

class RewardDynamics(Scene):
    def construct(self):
        # Create grid
        grid = VGroup(*[Square(color=WHITE) for _ in range(9)])
        grid.arrange_in_grid(rows=3, columns=3)
        
        # Place center pixel
        center_pixel = Square(color=RED).scale(1.2)
        
        # Place neighbors
        top_left = grid[0].next_to(center_pixel, LEFT)
        top_right = grid[2].next_to(center_pixel, RIGHT)
        bottom_left = grid[6].next_to(center_pixel, LEFT).shift(DOWN)
        bottom_right = grid[8].next_to(center_pixel, RIGHT).shift(DOWN)
        
        # Arrange neighbors
        neighbors = VGroup(top_left, top_right, bottom_left, bottom_right)
        
        # Place grid and center pixel
        self.add(grid)
        self.play(Transform(center_pixel, BLUE))
        
        # Narration
        narration = Text("In reinforcement learning, the agent learns by flipping pixels and observing\nthe immediate change in border length.").scale(0.7).to_edge(DOWN, buff=1)
        self.play(FadeIn(narration), run_time=2)
        
        # Flip the center pixel to Blue
        self.play(Transform(center_pixel, BLUE), run_time=1)
        
        # Highlight new borders
        new_border = Rectangle(color=GREEN).next_to(center_pixel, RIGHT)
        self.play(Create(new_border), run_time=1)
        
        # Highlight lost borders
        lost_border = Line(color=RED).next_to(center_pixel, LEFT)
        self.play(Create(lost_border), run_time=1)

        # Update the reward
        reward_text = Text("+2").next_to(center_pixel, UP)
        self.play(Create(reward_text), run_time=1)
        
        # Update the cumulative reward (BarChart for simplicity)
        bar = Rectangle(width=3, color=BLUE).next_to(center_pixel, RIGHT).shift(DOWN)
        self.play(Create(bar), run_time=1)

        # Narration
        self.play(FadeOut(reward_text), run_time=1)
        narration = Text("If a flip creates more red-blue boundaries, the agent receives\na positive reward proportional to that increase.").to_edge(DOWN)
        self.play(Transform(narration, Text("If a flip creates more red-blue boundaries, the agent receives\na positive reward proportional to that increase.").scale(0.7)))
        
        # Narration
        self.play(FadeOut(narration), run_time=1)
        narration = Text("If it reduces the boundary, it's penalized.").to_edge(DOWN)
        self.play(Transform(narration, Text("If it reduces the boundary, it's penalized.").scale(0.7)))
        
        # Narration
        self.play(FadeIn(narration), run_time=1)
        narration = Text("This turns a spatial arrangement problem into a sequence of\nvalue-driven decisions.").to_edge(DOWN)
        self.play(Transform(narration, Text("This turns a spatial arrangement problem into a sequence of\nvalue-driven decisions.").scale(0.7)))
        
        # Final narration
        narration = Text("The formula used for this is: R_t = Border_{t} - Border_{t-1}").to_edge(DOWN)
        self.add(narration, run_time=2)
        
        # Wait for completion
        self.wait()