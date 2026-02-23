from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle(radius=1)
        self.play(Create(circle))
        self.wait()