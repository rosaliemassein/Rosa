from manim import *

class SimpleTextScene(Scene):
    def construct(self):
        text = Text("Hello, Manim!")
        self.play(Create(text))
        self.wait(2)
        self.play(FadeOut(text))
        self.wait(1)