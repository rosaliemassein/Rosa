from manim import *

class ParameterVsDataBottleneck(Scene):
    def construct(self):
        # Title
        title = MathTex(r"\text{Why did the simple LWR outperform a powerful Neural Network?}")
        title.to_edge(UP)
        
        # Voice text
        voice_text = Text("It comes down to data. With only 27 training points, the Neural Network's 24 internal parameters were prone to 'overfitting'—it was essentially memorizing the noise rather than learning the physics. LWR, being a local linear approximation, was much more robust to this small sample size.")
        voice_text.next_to(title, DOWN).shift(DOWN)
        
        # Neural Network plot
        nn_plot = VGroup(
            Line(start=(-2, -0.5, 0), end=(0, 1, 0)).set_color(RED),
            Line(start=(0, 1, 0), end=(2, -0.5, 0)).set_color(RED)
        )
        nn_plot.shift(RIGHT * 3).scale(0.5)
        
        # LWR plot
        lwr_plot = VGroup(
            Line(start=(-2, -0.5, 0), end=(0, 1, 0)).set_color(BLUE),
            Line(start=(0, 1, 0), end=(2, -0.5, 0)).set_color(BLUE)
        )
        lwr_plot.shift(RIGHT * 3).scale(0.5)
        
        # MSE text
        mse_text = MathTex(r"MSE = \frac{||Y_{test} - Y_{pred}||_F^2}{3n}")
        mse_text.shift(DOWN * 2)
        
        # MSE values
        nn_mse = MathTex(r"1.21").next_to(mse_text, RIGHT)
        lwr_mse = MathTex(r"0.85").next_to(mse_text, LEFT)
        
        # Animation
        self.play(Write(title))
        self.wait()
        self.play(Create(voice_text), run_time=2)
        self.wait(3)
        self.play(FadeIn(nn_plot, lwr_plot))
        self.wait()
        self.play(Transform(lwr_plot, nn_plot), run_time=1)
        self.wait()
        self.play(Write(mse_text))
        self.wait()
        self.play(FadeIn(nn_mse, lwr_mse))
        self.wait()