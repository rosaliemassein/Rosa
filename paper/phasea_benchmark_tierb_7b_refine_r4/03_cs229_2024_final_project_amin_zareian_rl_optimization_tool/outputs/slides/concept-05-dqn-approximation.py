from manim import *

class Concept05DQNApproximation(Scene):
    def construct(self):
        # Create the 5x5 pixel grid
        pixels = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange_in_grid(rows=5, cols=5)
        pixels.shift(LEFT * 2)

        # Animate the pixel grid flattening into a 1D vector
        flat_vector = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange(RIGHT, buff=0.2)
        flat_vector.shift(RIGHT * 6)

        self.play(FadeIn(pixels))
        self.wait(1)
        self.play(Transform(pixels, flat_vector))
        self.wait()

        # Input layer of Neural Network
        input_layer = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange(RIGHT, buff=0.2)
        input_layer.shift(DOWN * 3)

        # Neural Network connections
        connection_lines = VGroup(*[Line(start=input_layer[i].get_center(), end=Dot(radius=0.1).shift(RIGHT * 3 + UP * 1).get_center()) for i in range(25)])
        output_layer = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange(RIGHT, buff=0.2)
        output_layer.shift(RIGHT * 3 + UP * 1)

        self.play(FadeIn(input_layer), FadeIn(connection_lines), LaggedStart(*[Create(output_layer[i]) for i in range(25)]))
        self.wait()

        # Highlight the output node with the highest value
        max_value = 4  # Assume the max value is 4 for demonstration
        max_dot = output_layer[max_value]
        self.play(Flash(max_dot, color=RED), Indicate(max_dot, color=RED))
        self.wait()

        # Flip the corresponding pixel in the original grid
        flipped_pixel = pixels[max_value]
        self.play(Transform(flipped_pixel, Dot(radius=0.1).set_color(RED)), run_time=2)
        self.wait()

        # Show Q(s, a; θ) ≈ Q*(s, a)
        formula = MathTex(r"Q(s, a; \theta) \approx Q^*(s, a)").shift(UP * 3)
        self.play(FadeIn(formula))
        self.wait()