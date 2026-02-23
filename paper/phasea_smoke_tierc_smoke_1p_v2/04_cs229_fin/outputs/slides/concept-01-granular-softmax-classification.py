from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # Load image
        plastic_bottle = ImageMobject("img-12.jpeg").scale(0.5)
        self.play(FadeIn(plastic_bottle))
        self.wait(1)

        # Draw CNN layers
        cnn_layers = VGroup(*[Rectangle(width=2, height=0.5) for _ in range(3)]).arrange(RIGHT, buff=1)
        cnn_layers.shift(DOWN)
        self.play(Create(cnn_layers))
        self.wait(1)

        # Data flow arrows
        data_flow = VGroup(
            Arrow(cnn_layers[0].get_bottom(), cnn_layers[1].get_top()),
            Arrow(cnn_layers[1].get_bottom(), cnn_layers[2].get_top())
        )
        self.play(Create(data_flow))
        self.wait(1)

        # Input vector
        input_vector = VGroup(*[MathTex(r"x_i").shift(RIGHT * i) for i in range(3)])
        input_vector.shift(DOWN * 2.5)
        self.play(Create(input_vector))
        self.wait(1)

        # Softmax formula
        softmax_formula = MathTex(r"\text{softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}")
        softmax_formula.shift(RIGHT * 4.5)
        self.play(Create(softmax_formula))
        self.wait(2)

        # Raw values
        raw_values = VGroup(*[MathTex(r"x_i").shift(RIGHT * (i - 3) + DOWN * 1.5) for i in range(6, 9)])
        self.play(Create(raw_values))
        self.wait(1)

        # Summation
        summation = MathTex(r"\sum_{j=1}^{n} e^{x_j}")
        summation.shift(RIGHT * 4.5 + DOWN * 0.5)
        self.play(Create(summation))
        self.wait(1)

        # Bar chart
        bar_chart = VGroup(*[Rectangle(width=0.4, height=0.2 * i) for i in range(1, 6)]).arrange(RIGHT, buff=0.2)
        bar_chart.shift(DOWN * 3.5)
        self.play(Create(bar_chart))
        self.wait(1)

        # Indicate highest bar
        highlight = SurroundingRectangle(bar_chart[0], color=BLUE, buff=-0.1)
        self.play(Create(highlight))
        self.wait(1)

        # Label highest bar
        label = MathTex(r"\text{Plastic Bottle}").next_to(highlight, DOWN)
        self.play(Create(label))
        self.wait(1)

        # Clean up
        self.play(FadeOut(plastic_bottle, data_flow, softmax_formula, raw_values, summation, bar_chart, highlight, label))
        self.wait(1)