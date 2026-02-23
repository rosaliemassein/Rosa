from manim import *

class OpponentAbstraction(Scene):
    def construct(self):
        # 2-player board with Blue and Red
        blue_square = Square(color=BLUE, fill_opacity=0.7)
        red_square = Square(color=RED, fill_opacity=0.7)
        blue_square.shift(LEFT * 1.5)
        red_square.shift(RIGHT * 1.5)

        # Animation to merge 5 opponents into a single 'Red' intensity
        opponent_layer = Square(color=RED, fill_opacity=0.7)
        opponent_layer.shift(UP)

        self.play(Create(blue_square), Create(red_square))
        self.wait(1)
        
        self.play(FadeOut(blue_square), FadeOut(red_square))
        self.wait(1)
        
        self.play(Create(opponent_layer), run_time=2)
        self.wait(1)
        
        # Cross-out individual identities
        cross_out_text = Text("Cross-OUT", font_size=30)
        cross_out_text.next_to(opponent_layer, DOWN)
        
        self.play(Create(cross_out_text))
        self.wait(1)
        
        # Check mark over unified 'Opponent Layer'
        check_mark = MathTex(r"\checkmark", color=GREEN, font_size=50)
        check_mark.next_to(opponent_layer, DOWN)

        self.play(Transform(cross_out_text, check_mark), run_time=1)
        self.wait(2)