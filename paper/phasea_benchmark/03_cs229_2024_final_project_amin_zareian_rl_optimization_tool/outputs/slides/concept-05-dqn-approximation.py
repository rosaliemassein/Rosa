from manim import *

class Concept05DQNApproximation(Scene):
    def construct(self):
        # Draw the 5x5 pixel grid
        pixel_grid = VGroup(*[
            Circle(color=WHITE, fill_color=YELLOW, radius=0.15)
            for i in range(25)
        ])
        pixel_grid.arrange_in_grid(5)
        self.play(Create(pixel_grid))
        self.wait()

        # Narration: Flattening the grid
        text = Text("Flattening the pixel grid into a 1D vector of 25 values (0s and 1s).", font_size=24, color=YELLOW)
        self.play(Write(text), run_time=2)
        self.wait()

        # Animation: Flattening process
        for i in range(25):
            self.play(Transform(
                pixel_grid[i], 
                Dot(color=WHITE, point=pixel_grid[i].get_center(), radius=0.15)
            ))
        self.wait()

        # Narration: Flattened vector
        text = Text("These values flow into an input layer of a Neural Network (circles and lines).", font_size=24, color=YELLOW)
        self.play(Transform(text, Write(text)), run_time=2)
        self.wait()

        # Drawing the input layer
        input_layer = VGroup(*[
            Line(color=GREEN, stroke_width=3)
            for i in range(25)
        ])
        input_layer.arrange_in_grid(5, 5)
        self.play(Create(input_layer), run_time=2)
        self.wait()

        # Narration: Output layer
        output_layer = VGroup(*[
            Dot(color=RED, point=[-2.5, -3.5, 0], radius=0.1)
            for i in range(25)
        ])
        output_layer.arrange_in_grid(5, 5)
        self.play(Create(output_layer), run_time=2)
        self.wait()

        # Highlighting the output node with the highest value
        max_value_node = Dot(color=RED, point=[-2.5, -3.0, 0], radius=0.1)
        max_value_node.scale(1.2)
        self.play(Transform(output_layer[0], max_value_node), run_time=1)

        # Narration: Flipped pixel
        flipped_pixel = Dot(color=GREEN, point=[-2.5, -3.0, 0], radius=0.1)
        flipped_pixel.scale(1.2)
        self.play(Transform(max_value_node, flipped_pixel), run_time=1)

        # Narration: Final result
        text = Text("The output node with the highest value is highlighted. The corresponding pixel in the original grid flips.", font_size=24, color=YELLOW)
        self.play(Transform(text, Write(text)), run_time=2)
        self.wait()

        # Final narration
        text = Text("This process replaces tabular RL with Deep RL for pixel optimization.", font_size=24, color=YELLOW)
        self.play(Transform(text, Write(text)), run_time=2)
        self.wait()

        # Final frame
        self.play(FadeOut(text))