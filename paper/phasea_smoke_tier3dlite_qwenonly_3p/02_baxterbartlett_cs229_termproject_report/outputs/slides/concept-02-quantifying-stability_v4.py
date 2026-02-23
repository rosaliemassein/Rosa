from manim import *

class ExampleScene(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=2, color=RED)
        self.play(Create(circle))
        self.play(Transform(circle, square))
        self.wait(2)