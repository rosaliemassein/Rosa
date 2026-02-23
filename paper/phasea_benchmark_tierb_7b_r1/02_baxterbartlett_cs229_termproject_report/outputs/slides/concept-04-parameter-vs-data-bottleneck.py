from manim import *

class ParameterVsDataBottleneck(Scene):
    def construct(self):
        # Create titles and text
        title = Text("Why did the simple LWR outperform a powerful Neural Network?")
        explanation = Text(
            "It comes down to data. With only 27 training points, the Neural Network's 24 internal parameters were prone to 'overfitting'—it was essentially memorizing the noise rather than learning the physics. LWR, being a local linear approximation, was much more robust to this small sample size."
        ).scale(0.8)

        # Show side-by-side plots
        neural_network = Text("Neural Network").to_edge(UP)
        lwr = Text("LWR").next_to(neural_network, DOWN)
        neural_network_plot = VGroup(Arrow(LEFT, RIGHT), Text("High Variance").to_edge(DOWN))
        lwr_plot = VGroup(Arrow(LEFT, RIGHT), Text("Smooth").to_edge(DOWN))
        neural_network_plot.shift(RIGHT * 2.5)
        lwr_plot.shift(RIGHT * 0.5)

        # Animation for plots
        self.play(FadeIn(neural_network), FadeIn(lwr))
        self.wait(1)
        self.play(Create(VGroup(*neural_network_plot)), Create(VGroup(*lwr_plot)))
        self.wait(1)

        # Show bar chart
        mse_label = MathTex(r"MSE").scale(0.8)
        neural_network_bar = Rectangle(height=1.21, width=0.5).next_to(mse_label, DOWN)
        lwr_bar = Rectangle(height=0.85, width=0.5).next_to(neural_network_bar, DOWN)
        mse_label.shift(RIGHT * 0.25 + UP * 0.1)

        # Animation for bar chart
        self.play(Create(mse_label), Create(neural_network_bar), Create(lwr_bar))
        self.wait(2)