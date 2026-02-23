from manim import *

class SemanticEmbeddingScene(Scene):
    def construct(self):
        # 1. Setup - Using basic Line objects instead of NumberPlane or ThreeDAxes
        # to adhere to constrained subset restrictions.
        x_axis = Line(LEFT * 5, RIGHT * 5, color=GREY_B)
        y_axis = Line(DOWN * 3.5, UP * 3.5, color=GREY_B)
        self.add(x_axis, y_axis)

        # 2. Key Concepts and Coordinates (2D space)
        loc_dl = [2, 1.5, 0]
        loc_nn = [2.5, 0.5, 0]
        loc_rb = [-2.5, -1.5, 0]

        label_dl = Text("Deep Learning", font_size=24).move_to(loc_dl).shift(UP * 0.4)
        label_nn = Text("Neural Networks", font_size=24).move_to(loc_nn).shift(UP * 0.4)
        label_rb = Text("Robotics", font_size=24).move_to(loc_rb).shift(UP * 0.4)

        # Animation: Floating text labels pop up
        self.play(Write(label_dl), Write(label_nn), Write(label_rb))
        self.wait(0.5)

        # 3. Transform labels into Dot objects
        dot_dl = Dot(loc_dl, color=BLUE)
        dot_nn = Dot(loc_nn, color=BLUE)
        dot_rb = Dot(loc_rb, color=RED)

        self.play(
            ReplacementTransform(label_dl, dot_dl),
            ReplacementTransform(label_nn, dot_nn),
            ReplacementTransform(label_rb, dot_rb)
        )
        self.wait(0.5)

        # 4. Show distance/similarity (Using Line as DashedLine is disallowed)
        similarity_line = Line(loc_dl, loc_nn, color=YELLOW)
        self.play(Create(similarity_line))
        self.wait(1)

        # 5. Display the formula
        formula = MathTex(r"v_{\text{phrase}} = \frac{1}{n} \sum_{i=1}^{n} v_{i}").scale(0.8)
        formula.to_corner(UL)
        self.play(Write(formula))
        self.wait(1)

        # 6. Multi-word phrase averaging demo: "Machine" and "Learning"
        # Positioning them in the upper-left quadrant
        loc_machine = [-1.5, 2.5, 0]
        loc_learning = [-3.5, 2.5, 0]
        loc_average = [-2.5, 2.5, 0]

        word_machine = Text("Machine", font_size=22).move_to(loc_machine).shift(UP * 0.4)
        dot_machine = Dot(loc_machine, color=GREEN)
        word_learning = Text("Learning", font_size=22).move_to(loc_learning).shift(UP * 0.4)
        dot_learning = Dot(loc_learning, color=GREEN)

        self.play(FadeIn(word_machine), Create(dot_machine))
        self.play(FadeIn(word_learning), Create(dot_learning))
        self.wait(1)

        # 7. Merge individual word vectors into the phrase vector (average)
        dot_phrase = Dot(loc_average, color=YELLOW)
        label_phrase = Text("Machine Learning", font_size=22).move_to(loc_average).shift(UP * 0.4)

        self.play(
            ReplacementTransform(dot_machine, dot_phrase),
            ReplacementTransform(dot_learning, dot_phrase),
            ReplacementTransform(word_machine, label_phrase),
            ReplacementTransform(word_learning, label_phrase)
        )
        self.wait(2)