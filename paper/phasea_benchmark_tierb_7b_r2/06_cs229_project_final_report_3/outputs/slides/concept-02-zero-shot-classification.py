from manim import *

class ZeroShotClassification(Scene):
    def construct(self):
        # Create vector 'v' representing the image
        v = Arrow(start=(-3, 0), end=(1, 0), color=BLUE)
        self.play(Create(v))
        self.wait(1)

        # Create matrix 'X' where each row is a country name
        X = VGroup(*[Text(country, color=BLACK).shift(RIGHT * i) for i, country in enumerate(["France", "Germany", "Italy", "Spain"])])
        X.arrange(RIGHT, buff=2)
        X.shift(LEFT * 3)
        self.play(Create(X))
        self.wait(1)

        # Pulsing highlight for dot product operation
        highlight = SurroundingRectangle(v, color=RED)
        self.play(Create(highlight))
        for _ in range(3):
            self.play(highlight.animate.scale(1.2).scale(0.8), runtime=0.5)
        self.play(FadeOut(highlight))
        self.wait(1)

        # Example dot product results
        results = VGroup(*[Text(f"{country}: 0.5", color=GREEN) for country in ["France", "Germany", "Italy", "Spain"]])
        results.arrange(RIGHT, buff=2)
        results.shift(LEFT * 3, UP * 1.5)
        self.play(Create(results))
        self.wait(1)

        # Real-time bar chart update
        bars = VGroup(*[Rectangle(height=value, width=0.2, color=BLUE).next_to(country, DOWN) for country, value in zip(X, [0.5, 0.3, 0.7, 0.4])])
        self.play(FadeIn(bars))
        for country, bar in zip(X, bars):
            bar.animate.set_height(max(0.1, bar.height + 0.2))
        self.wait(1)

        # Transform dot product expression into final probability vector
        formula = MathTex(r"h(\mathbf{v};\mathbf{X})=\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}")
        formula.shift(DOWN * 2)
        self.play(Create(formula))
        self.wait(2)

        # Clean up
        self.play(FadeOut(v), FadeOut(X), FadeOut(results), FadeOut(bars), FadeOut(formula))
        self.wait(1)