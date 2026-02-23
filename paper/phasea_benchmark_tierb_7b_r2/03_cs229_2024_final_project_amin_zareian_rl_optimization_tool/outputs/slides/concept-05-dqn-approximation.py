from manim import *

class PixelOptimizationAnimation(Scene):
    def construct(self):
        # Create a 5x5 grid of pixels
        pixel_grid = VGroup(*[
            Dot().shift(RIGHT * 2.5 * i + DOWN * 2.5 * j)
            for i in range(5) for j in range(5)
        ])
        pixel_grid.arrange_in_grid(rows=5, cols=5)

        # Flatten the grid into a 1D vector
        flat_vector = VGroup(*[
            Dot().shift(RIGHT * i + DOWN * j)
            for i in range(25)
        ])
        flat_vector.arrange_in_grid(rows=5, cols=5)

        # Create a neural network input layer
        input_layer = VGroup(*[
            Circle(radius=0.1).shift(RIGHT * 2.5 * (i % 5) + DOWN * 2.5 * (i // 5))
            for i in range(25)
        ])
        input_layer.arrange_in_grid(rows=5, cols=5)

        # Connect the flat vector to the input layer
        for i in range(25):
            self.play(Transform(flat_vector[i], input_layer[i]))

        # Create the output layer
        outputs = VGroup(*[
            MathTex(r"Q(s, a_{}; \theta)".format(i+1), color=RED).shift(RIGHT * 3.5 + DOWN * (i - 10) * 0.75)
            for i in range(25)
        ])
        outputs.arrange_in_grid(rows=5, cols=5)

        # Highlight the output node with the highest value
        max_index = 12  # Example index for the highest value
        self.play(FadeIn(outputs[max_index]))

        # Show that corresponding pixel in the original grid flipping
        pixel_to_flip = pixel_grid[max_index]
        self.play(FadeOut(pixel_to_flip), Create(pixel_to_flip.copy().set_color(BLUE)))

        # Fade out all other elements
        self.wait(2)
        for mobject in self.mobjects:
            self.play(FadeOut(mobject))