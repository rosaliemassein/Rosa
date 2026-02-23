from manim import *

class ConceptRewardDynamics(Scene):
    def construct(self):
        # Create a 3x3 grid
        grid = VGroup(
            *[Dot(color=BLUE) for _ in range(9)]
        ).arrange_in_grid(rows=3, cols=3)

        # Initialize the center pixel
        center_pixel = Dot(color=RED)
        self.add(grid, center_pixel)

        # Define the neighbors of the center pixel
        neighbors = [
            grid[0] * 2,  # Top neighbor
            grid[1],         # Right neighbor
            grid[2] * 2,  # Bottom neighbor
            grid[3],         # Left neighbor
        ]

        # Create a line for the center pixel's border
        center_line = Line(center_pixel.get_center(), neighbors[0].get_center())

        # Function to update the border
        def update_border():
            center_pixel.set_color(BLUE)
            self.circle_to_polygon(center_pixel, neighbors[0], color=RED)
            center_line.set_color(RED)

        # Update the border of the center pixel
        self.play(update_border, run_time=2)

        # Narration at the end of the animation
        self.play(FadeIn(Text(self.voice)), run_time=1)