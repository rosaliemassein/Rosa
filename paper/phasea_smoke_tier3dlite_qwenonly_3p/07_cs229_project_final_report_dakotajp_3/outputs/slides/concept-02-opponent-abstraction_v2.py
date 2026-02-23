from manim import *

class SimpleScene(Scene):
    def construct(self):
        text = Text("Hello, Manim!", color=BLUE)
        self.play(Create(text))
        self.wait(2)