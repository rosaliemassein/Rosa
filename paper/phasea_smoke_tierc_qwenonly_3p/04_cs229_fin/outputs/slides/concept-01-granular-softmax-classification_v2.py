from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # Create the plastic bottle image
        plastic_bottle = ImageMobject("img-12.jpeg").scale(0.5).to_edge(LEFT)
        self.play(FadeIn(plastic_bottle))
        
        # Draw CNN layers
        cnn_layers = VGroup(*[
            Rectangle(width=1, height=0.5).set_color(BLUE).shift(RIGHT * (i * 1.5))
            for i in range(5)
        ])
        self.play(Create(cnn_layers))
        
        # Arrow indicating data flow
        arrow = Arrow(start=plastic_bottle.get_right(), end=cnn_layers[0].get_left())
        self.play(Create(arrow))
        
        # Create column vector of raw values
        raw_values = VGroup(*[
            MathTex(f"x_{i}", color=RED).next_to(cnn_layers[4], DOWN) for i in range(1, 21)
        ])
        raw_values.arrange(DOWN).shift(RIGHT * 3.5, UP * 0.5)
        self.play(FadeIn(raw_values))
        
        # Softmax formula
        softmax_formula = MathTex(r"softmax(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{20} e^{x_j}}")
        softmax_formula.shift(RIGHT * 3.5, UP * 2)
        self.play(Create(softmax_formula))
        
        # Transform raw values into probabilities
        bar_chart = VGroup(*[
            Rectangle(width=0.4, height=0.2 * (1 / 20)).set_color(GREEN).shift(RIGHT * (3.5 + i * 0.5), UP)
            for i in range(20)
        ])
        self.play(Create(bar_chart))
        
        # Indicate the highest bar
        max_bar_index = 15  # Assuming x_15 is the maximum
        max_bar = bar_chart[max_bar_index]
        max_label = MathTex("Plastic Bottle").set_color(BLUE).next_to(max_bar, UP)
        self.play(Create(max_label), Indicate(max_bar))
        
        self.wait(2)