from manim import *

class SimpleBarChartExample(Scene):
    def construct(self):
        labels = [Text(f"{i}").next_to(Arrow(RIGHT, 0.5), LEFT) for i in range(1, 6)]
        bars = [Rectangle(height=i * 0.5, width=0.4) for i in range(1, 6)]
        bar_chart = VGroup(*bars + labels).arrange(RIGHT, buff=0.5)
        
        self.play(FadeIn(bar_chart))
        self.wait(2)