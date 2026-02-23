from manim import *

class BarChartExample(Scene):
    def construct(self):
        # Create axes
        x_axis = Axes(x_range=[0, 5], y_range=[0, 10])
        self.play(Create(x_axis))
        
        # Create bar chart data
        bars = VGroup()
        for i in range(1, 6):
            bar = Rectangle(height=i * 2, width=0.5).next_to(x_axis.get_x_axis(), DOWN)
            bars.add(bar)
        
        # Animation for bar chart appearance
        self.play(FadeIn(bars))
        self.wait()
        
        # Animation for scaling bars
        for bar in bars:
            self.play(Transform(bar, Rectangle(height=(i * 2) * 1.5, width=0.5)))
            self.wait(0.3)
        
        # Animation for removal of bars
        self.play(FadeOut(bars))
        self.wait()