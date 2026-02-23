from manim import *

class SoftmaxAnimation(Scene):
    def construct(self):
        # Load image
        bottle_image = ImageMobject("img-12.jpeg").scale(0.5).shift(LEFT * 4)

        # Create CNN layers
        cnn_layers = VGroup(*[Rectangle(color=BLUE, height=2, width=0.5).shift(RIGHT * i * 1.5) for i in range(3)])
        cnn_layers.arrange(DOWN, center=True)

        # Arrow showing data flow
        arrow = Arrow(start=cnn_layers[-1].get_right(), end=RIGHT * 3, color=RED)

        # Raw values
        raw_values = VGroup(*[MathTex(r"x_{{{i+1}}}", color=RED) for i in range(20)])
        raw_values.arrange(RIGHT, center=True).next_to(arrow.get_end(), LEFT)

        # Softmax function
        softmax_eq = MathTex(r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^n e^{x_j}}", color=GREEN)
        softmax_eq.shift(RIGHT * 3)

        # Bar chart
        bars = VGroup(*[Rectangle(height=0.5, width=0.4).set_color(color=GREEN) for _ in range(20)])
        bars.arrange(RIGHT, center=True).next_to(softmax_eq, RIGHT)

        # Animate
        self.play(Create(bottle_image), Create(cnn_layers), Create(arrow))
        self.wait()
        self.play(Create(raw_values))
        self.wait()
        self.play(Write(softmax_eq), Create(bars))
        self.wait()
        bars[0].set_color(color=BLUE)
        self.play(Transform(bars[0], bars[0].scale(1.2)), Indicate(bars[0]))
        self.wait()