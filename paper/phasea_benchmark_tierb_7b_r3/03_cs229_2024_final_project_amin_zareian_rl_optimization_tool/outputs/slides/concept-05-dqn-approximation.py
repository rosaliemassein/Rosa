from manim import *

class Concept05DQNApproximation(Scene):
    def construct(self):
        # Create a 5x5 pixel grid
        pixels = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange_in_grid(rows=5, cols=5)
        pixels.shift(RIGHT * 2)

        # Animate the grid 'flattening' into a 1D vector
        flat_pixels = pixels.copy().arrange(RIGHT, buff=0.2).to_edge(LEFT)
        self.play(Transform(pixels, flat_pixels))
        self.wait()

        # Create a neural network representation
        input_layer = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange(RIGHT, buff=0.2).to_edge(LEFT)
        input_layer.shift(DOWN * 1.5)
        output_layer = VGroup(*[Dot(radius=0.2, color=BLUE) for _ in range(5)]).arrange(RIGHT, buff=0.2).next_to(input_layer, DOWN)
        output_layer.shift(DOWN * 1.5)

        self.play(Create(input_layer), Create(output_layer))
        self.wait()

        # Connect input layer to output layer with arrows
        for i, dot in enumerate(input_layer):
            arrow = Arrow(start=dot.get_center(), end=output_layer[i].get_center(), color=YELLOW)
            self.play(Create(arrow))

        # Highlight the output node with the highest value
        max_output_index = 3  # Assuming it's the 4th node for example purposes
        max_output_node = output_layer[max_output_index]
        self.play(FadeIn(max_output_node), Indicate(max_output_node, color=RED))

        # Flip the corresponding pixel in the original grid
        pixel_to_flip = pixels[max_output_index]
        self.play(Transform(pixel_to_flip, Dot(radius=0.1, color=RED)))

        # Fade out the neural network representation
        self.play(FadeOut(input_layer), FadeOut(output_layer), FadeOut(max_output_node))
        self.wait()