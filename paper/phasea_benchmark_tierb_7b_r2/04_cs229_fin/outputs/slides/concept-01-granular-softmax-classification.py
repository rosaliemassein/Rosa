from manim import *

class Concept01GranularSoftmaxClassification(Scene):
    def construct(self):
        # Load the image
        bottle_image = ImageMobject("img-12.jpeg")
        bottle_image.scale(0.5)
        bottle_image.to_edge(LEFT)

        # Vertical rectangles representing CNN layers
        cnn_layers = VGroup(
            Rectangle(height=2, width=0.5),
            Rectangle(height=1.5, width=0.5),
            Rectangle(height=1, width=0.5)
        ).arrange(DOWN).next_to(bottle_image, RIGHT)

        # Arrows showing data flow
        arrows = VGroup(
            Arrow(start=bottle_image.get_right(), end=cnn_layers[0].get_left()),
            Arrow(start=cnn_layers[-1].get_right(), end=RIGHT * 4)
        ).set_color(BLUE)

        # Raw values representing neural network outputs
        raw_values = VGroup(
            MathTex(r'x_1', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_2', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_3', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_4', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_5', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_6', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_7', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_8', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_9', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{10}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{11}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{12}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{13}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{14}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{15}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{16}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{17}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{18}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{19}', color=RED).next_to(arrows[1], RIGHT, buff=0.5),
            MathTex(r'x_{20}', color=RED).next_to(arrows[1], RIGHT, buff=0.5)
        ).arrange(RIGHT, buff=0.7)

        # Softmax formula appearing
        softmax_formula = MathTex(r"softmax(x_{i})=\frac{e^{x_{i}}}{\sum_{j=1}^{n}e^{x_{j}}}", color=GREEN).to_edge(RIGHT * 3)

        # Bar chart transforming raw values into probabilities
        probabilities = VGroup(
            Rectangle(height=0.5, width=0.2),
            Rectangle(height=1.0, width=0.2),
            Rectangle(height=1.5, width=0.2),
            Rectangle(height=2.0, width=0.2),
            Rectangle(height=1.5, width=0.2),
            Rectangle(height=1.0, width=0.2),
            Rectangle(height=0.5, width=0.2),
            Rectangle(height=1.0, width=0.2),
            Rectangle(height=1.5, width=0.2),
            Rectangle(height=2.0, width=0.2),
            Rectangle(height=1.5, width=0.2),
            Rectangle(height=1.0, width=0.2),
            Rectangle(height=0.5, width=0.2),
            Rectangle(height=1.0, width=0.2),
            Rectangle(height=1.5, width=0.2),
            Rectangle(height=2.0, width=0.2),
            Rectangle(height=1.5, width=0.2),
            Rectangle(height=1.0, width=0.2),
            Rectangle(height=0.5, width=0.2)
        ).arrange(RIGHT, buff=0.7).next_to(softmax_formula, RIGHT)

        # Indicate the highest bar and label it 'Plastic Bottle'
        self.play(Create(bottle_image))
        self.wait(1)
        for layer in cnn_layers:
            self.play(Create(layer), run_time=0.5)
            self.wait(0.5)
        for arrow in arrows:
            self.play(Create(arrow), run_time=0.5)
            self.wait(0.5)
        for value in raw_values:
            self.play(FadeIn(value), run_time=0.2)
        for bar in probabilities:
            self.play(Create(bar), run_time=0.1)
        self.play(Indicate(probabilities[3], color=BLUE))
        bar = probabilities[3]
        self.play(Transform(bar, Text("Plastic Bottle").scale(0.5)), run_time=0.5)
        self.wait(2)