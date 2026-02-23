from manim import *

class ExampleScene(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        text = Text("Hello, Manim!", font_size=24)
        self.play(Create(circle), Write(text))
        self.wait(1)