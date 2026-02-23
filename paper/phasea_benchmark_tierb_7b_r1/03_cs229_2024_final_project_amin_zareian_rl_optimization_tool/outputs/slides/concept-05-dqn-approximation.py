from manim import *

class Concept05DQNApproximation(Scene):
    def construct(self):
        # Create 5x5 grid
        pixels = VGroup(*[Square().scale(0.2) for _ in range(25)]).arrange_in_grid(rows=5, cols=5)
        pixels.shift(RIGHT*2)

        # Connect pixels to input layer of neural network
        network_input = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange(RIGHT, buff=1)
        network_input.shift(DOWN*4)

        # Highlight connections
        connections = VGroup(*[Line(pixels[i], network_input[i]) for i in range(25)])
        self.play(LaggedStart(*[Create(connection) for connection in connections]))
        self.wait()

        # Neural network layers
        hidden_layer = VGroup(*[Dot(radius=0.1) for _ in range(3)]).arrange(RIGHT, buff=1)
        output_layer = VGroup(*[Dot(radius=0.1) for _ in range(25)]).arrange(RIGHT, buff=1)
        hidden_layer.shift(DOWN*2.5)
        output_layer.shift(DOWN*.5)

        # Connect layers
        self.play(LaggedStart(*[Create(Line(hidden_layer[i], output_layer[i])) for i in range(3)]))
        self.wait()

        # Highlight output layer nodes
        max_node = output_layer[0]
        for node in output_layer:
            if node is not max_node:
                self.play(node.animate.set_color(GREY))
        self.wait()

        # Flip corresponding pixel
        flipped_pixel = pixels[0]
        self.play(flipped_pixel.animate.set_color(RED))
        self.wait()