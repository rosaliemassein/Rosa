from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # Image of a plastic bottle
        bottle_image = ImageMobject("img-12.jpeg").scale(0.5)
        self.play(FadeIn(bottle_image), run_time=2)

        # CNN layers
        cnn_layers = VGroup(*[Rectangle(width=0.5, height=1, color=BLUE) for _ in range(3)])
        cnn_layers.arrange(DOWN, center=True).to_right()
        self.play(Create(cnn_layers), run_time=1)

        # Arrow showing data flow
        arrow = Arrow(start=bottle_image.get_bottom(), end=cnn_layers.get_top())
        self.play(Create(arrow), run_time=0.5)

        # Raw values from CNN layers
        raw_values = [MathTex(r"x_{{{} {}}} = 0.5".format(i, chr(65+i))) for i in range(3)]
        raw_values.arrange(RIGHT, center=True).next_to(cnn_layers, LEFT)
        self.play(Create(VGroup(*raw_values)), run_time=1)

        # Softmax formula
        softmax_formula = MathTex(r"\sigma(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{n} e^{x_j}}")
        softmax_formula.to_edge(RIGHT, buff=2)
        self.play(Create(softmax_formula), run_time=1)

        # Probability distribution
        probabilities = [MathTex(r"p_i").scale(0.75) for _ in range(3)]
        probability_values = [MathTex(r"0.25") for _ in range(3)]
        probability_bars = VGroup(*[Rectangle(width=1, height=p.get_value(), color=RED) for p in probability_values])
        probabilities.arrange(RIGHT, center=True).next_to(probability_bars, DOWN)
        probability_values.arrange(RIGHT, center=True).next_to(probability_bars, UP)

        bar_chart = VGroup(*[VGroup(bar, prob_text) for bar, prob_text in zip(probability_bars, probabilities)])
        bar_chart.next_to(softmax_formula, RIGHT)
        self.play(Create(bar_chart), run_time=1)

        # Highlight the highest probability
        self.play(Indicate(probability_bars[0], color=GREEN), run_time=1)
        self.wait(2)