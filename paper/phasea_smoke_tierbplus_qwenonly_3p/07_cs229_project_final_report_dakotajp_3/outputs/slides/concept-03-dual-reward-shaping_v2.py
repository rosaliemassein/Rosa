from manim import *

class ExampleScene(Scene):
    def construct(self):
        text = Text("Hello, Manim!")
        self.play(Create(text))
        self.wait(2)
        new_text = Text("Goodbye, Manim!")
        self.play(Transform(text, new_text))
        self.wait(2)
        self.play(FadeOut(new_text))
        self.wait()