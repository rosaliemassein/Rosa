from manim import *

class ExampleScene(Scene):
    def construct(self):
        rectangle = Rectangle(color=BLUE).scale(1.5)
        self.play(Create(rectangle))
        self.wait(2)