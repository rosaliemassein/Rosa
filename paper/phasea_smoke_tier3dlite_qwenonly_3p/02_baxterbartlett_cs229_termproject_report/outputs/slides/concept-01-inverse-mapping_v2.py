from manim import *

class CompilingScene(Scene):
    def construct(self):
        text = Text("Hello, World!")
        self.play(Create(text))
        self.wait(1)
        arrow = Arrow(start=text.get_center() + 2*RIGHT, end=text.get_center() + 4*RIGHT)
        self.play(Create(arrow))
        self.wait(1)