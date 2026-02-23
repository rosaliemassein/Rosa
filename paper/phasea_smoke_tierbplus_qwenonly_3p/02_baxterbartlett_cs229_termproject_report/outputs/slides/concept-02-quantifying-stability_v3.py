from manim import *

class ExampleScene(Scene):
    def construct(self):
        self.play(Create(Text("Hello, World!")))
        self.wait(2)