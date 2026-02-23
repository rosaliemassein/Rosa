from manim import *

class ExampleScene(Scene):
    def construct(self):
        text = Text("Hello, Manim!")
        self.play(Create(text))
        self.wait(2)