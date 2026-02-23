from manim import *

class ExampleScene(Scene):
    def construct(self):
        # your code here
        text = Text("Hello, Manim!")
        circle = Circle(radius=2)
        self.play(Create(text))
        self.wait(1)
        self.play(Transform(circle, Text("Manim is cool!")))
        self.wait()