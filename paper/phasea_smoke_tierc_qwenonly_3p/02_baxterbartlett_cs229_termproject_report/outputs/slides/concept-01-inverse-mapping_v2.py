from manim import *

class FixCode(Scene):
    def construct(self):
        text = Text("Corrected Code")
        self.play(Create(text))
        self.wait()