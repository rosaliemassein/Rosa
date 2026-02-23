from manim import *

class ConceptZeroShotClassification(Scene):
    def construct(self):
        v = Arrow(start=LEFT, end=RIGHT, color=YELLOW).move_to([-4, 0, 0])
        X = VGroup(*[Square(color=BLUE).move_to([i, -1 + (i % 2) * 0.75, 0]) for i in range(140)])
        X.arrange(RIGHT, buff=0.3)
        h = MathTex(r"h(\mathbf{v};\mathbf{X})=\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}", color=GREEN).move_to([2, 2, 0])

        self.play(Create(v), Write(h))
        self.wait()

        for i in range(140):
            dot_product = MathTex(r"\mathbf{X}_i \cdot \mathbf{v}", color=RED).move_to([-2, 1 + (i % 2) * 0.75, 0])
            self.play(Transform(v, dot_product))
            self.wait(0.1)
            result = MathTex(r"\exp(\mathbf{X}_i \cdot \mathbf{v})", color=BLUE).next_to(v, RIGHT)
            self.play(Transform(dot_product, result))
            self.wait(0.1)

        softmax = MathTex(r"\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}", color=GREEN).next_to(h, RIGHT, buff=2)
        self.play(Transform(h, softmax))
        self.wait()

        max_score = MathTex("France", color=RED).next_to(softmax, RIGHT)
        self.play(FadeIn(max_score))
        self.wait()

        for i in range(140):
            if i != 7:  # France is at index 7
                result = MathTex(r"\exp(\mathbf{X}_i \cdot \mathbf{v})", color=BLUE).move_to([2, 1 + (i % 2) * 0.75, 0])
                self.play(Transform(softmax[i].copy(), result))
                self.wait(0.1)

        self.wait()