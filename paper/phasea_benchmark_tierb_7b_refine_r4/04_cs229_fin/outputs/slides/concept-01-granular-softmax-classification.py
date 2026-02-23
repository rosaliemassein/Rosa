from manim import *

class GranularSoftmaxClassification(Scene):
    def construct(self):
        # Create input image and label
        bottle = ImageMobject("img-12.jpeg").scale(0.5)
        input_label = Text("Plastic Bottle")
        bottle_group = VGroup(bottle, input_label).arrange(DOWN).to_edge(LEFT)

        # Create CNN layers
        c1 = Rectangle(width=2, height=0.5).shift(LEFT * 3.5)
        c2 = Rectangle(width=1, height=0.5).shift(LEFT * 2.5)
        c3 = Rectangle(width=1, height=0.5).shift(LEFT * 2)

        # Create raw score values
        x1 = MathTex(r"e^{x_{1}}").set_color(GREEN).shift(LEFT * 4.5)
        x2 = MathTex(r"e^{x_{2}}").set_color(GREEN).shift(LEFT * 3.5)
        x3 = MathTex(r"e^{x_{3}}").set_color(GREEN).shift(LEFT * 3)
        x4 = MathTex(r"e^{x_{4}}").set_color(GREEN).shift(LEFT * 2.5)
        x5 = MathTex(r"e^{x_{5}}").set_color(GREEN).shift(LEFT * 2)
        x6 = MathTex(r"e^{x_{6}}").set_color(GREEN).shift(LEFT * 1.5)
        x7 = MathTex(r"e^{x_{7}}").set_color(GREEN).shift(LEFT * 1)
        x8 = MathTex(r"e^{x_{8}}").set_color(GREEN).shift(LEFT * 0.5)
        x9 = MathTex(r"e^{x_{9}}").set_color(GREEN).shift(RIGHT * 0.5)
        x10 = MathTex(r"e^{x_{10}}").set_color(GREEN).shift(RIGHT * 1)
        x11 = MathTex(r"e^{x_{11}}").set_color(GREEN).shift(RIGHT * 1.5)
        x12 = MathTex(r"e^{x_{12}}").set_color(GREEN).shift(RIGHT * 2)
        x13 = MathTex(r"e^{x_{13}}").set_color(GREEN).shift(RIGHT * 2.5)
        x14 = MathTex(r"e^{x_{14}}").set_color(GREEN).shift(RIGHT * 3)
        x15 = MathTex(r"e^{x_{15}}").set_color(GREEN).shift(RIGHT * 3.5)
        x16 = MathTex(r"e^{x_{16}}").set_color(GREEN).shift(RIGHT * 4)
        x17 = MathTex(r"e^{x_{17}}").set_color(GREEN).shift(RIGHT * 4.5)
        x18 = MathTex(r"e^{x_{18}}").set_color(GREEN).shift(RIGHT * 5)
        x19 = MathTex(r"e^{x_{19}}").set_color(GREEN).shift(RIGHT * 5.5)
        x20 = MathTex(r"e^{x_{20}}").set_color(GREEN).shift(RIGHT * 6)

        raw_scores = VGroup(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, 
                           x11, x12, x13, x14, x15, x16, x17, x18, x19, x20)

        # Animation
        self.play(Create(bottle_group))
        for layer in [c1, c2, c3]:
            self.play(Create(layer), run_time=0.5)
        self.wait(1)

        self.play(FadeIn(raw_scores))
        self.wait(2)

        # Indicate the highest bar
        max_score = MathTex(r"e^{x_{i}}", color=RED).next_to(x10, RIGHT)
        self.play(Indicate(x10), Write(max_score))
        self.wait(2)

        # Transform into probability distribution
        probabilities = VGroup(
            MathTex(r"\frac{e^{x_{1}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{2}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{3}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{4}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{5}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{6}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{7}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{8}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{9}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{10}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{11}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{12}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{13}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{14}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{15}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{16}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{17}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{18}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{19}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE),
            MathTex(r"\frac{e^{x_{20}}}{\sum_{j=1}^{20}e^{x_{j}}}").set_color(BLUE)
        )

        self.play(FadeOut(raw_scores), FadeIn(probabilities))
        self.wait(3)