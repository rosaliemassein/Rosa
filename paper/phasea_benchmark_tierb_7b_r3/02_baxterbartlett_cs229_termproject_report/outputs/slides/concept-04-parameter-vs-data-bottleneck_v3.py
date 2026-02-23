from manim import *

class ParameterVsDataBottleneck(Scene):
    def construct(self):
        # Left side: Neural Network
        neural_network_text = Text("Neural Network")
        neural_network_plot = VGroup(
            Line(start=(-3, 2.5, 0), end=(3, -1, 0)),
            Line(start=(-2.5, 2.5, 0), end=(-1.5, -1, 0)),
            Line(start=(1.5, -1, 0), end=(2.5, 2.5, 0)),
            Line(start=(-1.5, -1, 0), end=(3, -1, 0))
        ).scale(0.5)
        
        self.play(Create(neural_network_text))
        self.wait()
        self.play(FadeIn(neural_network_plot), Create(Circle(radius=0.1, color=RED).next_to(neural_network_plot[0], RIGHT)))
        self.wait()
        self.play(Create(Circle(radius=0.1, color=RED).next_to(neural_network_plot[2], RIGHT)))
        self.wait()
        
        # Right side: LWR
        lwr_text = Text("LWR")
        lwr_plot = VGroup(
            Line(start=(-3, 1.5, 0), end=(2, 1.5, 0)),
            Line(start=(-3, -2.5, 0), end=(2, -2.5, 0))
        ).scale(0.5)
        
        self.play(Create(lwr_text), Transform(neural_network_plot, lwr_plot))
        self.wait()
        self.play(Create(Circle(radius=0.1, color=BLUE).next_to(lwr_plot[0], RIGHT)))
        self.wait()
        
        # MSE Bar Chart
        mse_text = Text("MSE").to_edge(LEFT).shift(DOWN)
        mse_neural_network_bar = Rectangle(width=0.8, height=1.21, color=RED).next_to(mse_text, RIGHT)
        mse_lwr_bar = Rectangle(width=0.8, height=0.85, color=BLUE).next_to(mse_neural_network_bar, RIGHT)
        
        self.play(Create(mse_text), Create(mse_neural_network_bar), Create(mse_lwr_bar))
        self.wait()
        self.play(FadeOut(neural_network_text), FadeOut(lwr_text), FadeOut(lwr_plot))
        self.wait()