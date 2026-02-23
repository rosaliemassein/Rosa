from manim import *

class MyScene(Scene):
    def construct(self):
        # Create a simple square
        square = Square()
        self.play(Create(square))
        self.wait(1)

        # Transform the square into a circle
        circle = Circle()
        self.play(Transform(square, circle))
        self.wait(1)