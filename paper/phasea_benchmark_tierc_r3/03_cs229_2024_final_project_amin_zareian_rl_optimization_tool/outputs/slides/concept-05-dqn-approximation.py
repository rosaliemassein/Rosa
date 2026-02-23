from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # Create the 5x5 pixel grid
        pixel_grid = VGroup(*[
            Dot() for _ in range(25)
        ]).arrange_in_circle(ratio=0.7, buff=0.1, fill=False)

        # Flatten the pixel grid into a 1D vector
        vector = [MathTex(str(i)) for i in range(25)]
        vector.arrange_in_grid(rows=5, cols=5)

        # Create an input layer for the neural network
        input_layer = VGroup(*[
            Circle(color=BLUE, radius=0.1) for _ in range(25)
        ]).arrange_in_circle(ratio=0.7, buff=0.1, fill=False)

        # Create an output layer for the neural network
        output_layer = VGroup(*[
            Circle(color=GREEN, radius=0.1) for _ in range(25)
        ]).arrange_in_circle(ratio=0.7, buff=0.1, fill=False)

        # Connect input and output layers
        for i in range(25):
            arrow = Arrow(input_layer[i].get_center(), output_layer[i].get_corner(UR), buff=0)
            arrow.set_color(YELLOW)

        # Animate the flattening of
        self.play(Create(vector.copy()))
        self.wait(1)

        # Animate the input layer
        for i in range(25):
            self.play(FadeIn(input_layer[i]))
            self.wait()

        # Animate the output layer
        for i in range(25):
            self.play(Transform(input_layer[i], output_layer[i]))
            self.wait()
        
        # Highlight the node with the highest value
        max_value = 24  # Example value, replace with actual training process
        output_layer[max_value].set_color(RED)
        
        # Show the corresponding pixel flipping
        self.wait()
        flipped_pixel = Dot(color=RED).move_to(pixel_grid[max_value])
        self.play(Transform(input_layer[max_value], flipped_pixel))
        
        # Animate the arrow to the flipped pixel
        self.play(Transform(arrow, Arrow(input_layer[max_value].get_center(), flipped_pixel.get_corner(UR), buff=0.1)))
        
        # End narration
        self.wait(2)