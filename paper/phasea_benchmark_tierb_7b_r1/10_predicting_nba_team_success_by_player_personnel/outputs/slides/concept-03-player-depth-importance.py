from manim import *

class PlayerDepthImportance(Scene):
    def construct(self):
        players = VGroup(*[Circle(radius=0.5) for _ in range(10)]).arrange(RIGHT, buff=2)
        labels = VGroup(*[Text(f"{i+1}").next_to(players[i], UP) for i in range(10)])
        coefficients = VGroup(*[MathTex(r"\beta_" + str(i+1)).next_to(players[i], DOWN) for i in range(10)])

        self.play(Create(players), Create(labels), Create(coefficients))
        self.wait()

        first_two = VGroup(players[:2], coefficients[:2])
        fifth_eight = VGroup(players[4:6] + players[7:9], coefficients[4:6] + coefficients[7:9])

        self.play(first_two.animate.set_color(GOLD))
        self.wait()

        self.play(fifth_eight.animate.scale(1.2).shift(DOWN * 0.5), LaggedStart(*[Flash(coeff, color=BLUE) for coeff in coefficients[4:9]]))
        self.wait()

        self.play(FadeOut(first_two), FadeOut(fifth_eight))
        self.wait()