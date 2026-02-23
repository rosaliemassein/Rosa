from manim import *

class ExampleScene(Scene):
    def construct(self):
        circle = Circle(color=RED).scale(2)
        square = Square().next_to(circle, RIGHT)
        
        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(square, circle))
        self.wait(2)