from manim import *

class AverageCalculation(Scene):
    def construct(self):
        equation = MathTex(r"\text{average} = \frac{\text{sum of values}}{\text{number of values}}")
        self.play(Write(equation))
        self.wait(2)