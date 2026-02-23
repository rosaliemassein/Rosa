from manim import *
import numpy as np

class ContrastiveAlignment(Scene):
    def construct(self):
        # 1. Encoders
        img_enc = Rectangle(width=3, height=1.2, color=BLUE).shift(UP * 2 + LEFT * 3)
        img_enc_text = Text("Image Encoder", font_size=24).move_to(img_enc)
        
        txt_enc = Rectangle(width=3, height=1.2, color=RED).shift(DOWN * 2 + LEFT * 3)
        txt_enc_text = Text("Text Encoder", font_size=24).move_to(txt_enc)
        
        self.play(Create(img_enc), Write(img_enc_text))
        self.play(Create(txt_enc), Write(txt_enc_text))

        # 2. Inputs
        img_in = Text("Image: Street View France", font_size=20).next_to(img_enc, LEFT, buff=0.5)
        txt_in_correct = Text('"A photo in France"', font_size=20, color=YELLOW).next_to(txt_enc, LEFT, buff=0.5)
        
        self.play(FadeIn(img_in), Write(txt_in_correct))

        # 3. Embedding Space (Manual Axes)
        origin = RIGHT * 3
        x_axis = Line(origin + LEFT * 2, origin + RIGHT * 2, color=WHITE)
        y_axis = Line(origin + DOWN * 2, origin + UP * 2, color=WHITE)
        space_label = Text("Embedding Space", font_size=24).next_to(y_axis, UP)
        
        self.play(Create(x_axis), Create(y_axis), Write(space_label))

        # 4. Vectors
        # Initial state: Misaligned
        v_img = Arrow(origin, origin + [1.2, 1.2, 0], buff=0, color=BLUE)
        v_txt = Arrow(origin, origin + [-1.2, 0.5, 0], buff=0, color=RED)
        
        v_img_label = MathTex("v_{img}", color=BLUE).next_to(v_img.get_end(), UR, buff=0.1)
        v_txt_label = MathTex("v_{txt}", color=RED).next_to(v_txt.get_end(), UL, buff=0.1)

        self.play(GrowArrow(v_img), Write(v_img_label))
        self.play(GrowArrow(v_txt), Write(v_txt_label))
        self.wait(1)

        # 5. Similarity Score (Static text updates)
        sim_text = Text("Similarity:", font_size=24).to_edge(UP, buff=0.5).shift(RIGHT * 3)
        score = Text("0.12", font_size=32, color=YELLOW).next_to(sim_text, RIGHT)
        
        self.play(Write(sim_text), Write(score))

        # 6. Alignment Animation
        # Define target for text vector (same as image vector)
        target_v_txt = Arrow(origin, origin + [1.2, 1.2, 0], buff=0, color=RED)
        score_aligned = Text("0.98", font_size=32, color=YELLOW).next_to(sim_text, RIGHT)
        
        self.play(
            Transform(v_txt, target_v_txt),
            v_txt_label.animate.next_to(target_v_txt.get_end(), DR, buff=0.1),
            Transform(score, score_aligned),
            run_time=2
        )
        self.wait(1)

        # 7. Contrastive Step (Wrong Label)
        txt_in_wrong = Text('"A photo in Japan"', font_size=20, color=ORANGE).next_to(txt_enc, LEFT, buff=0.5)
        
        # New target for text vector (pushed away)
        pushed_v_txt = Arrow(origin, origin + [-0.8, -1.5, 0], buff=0, color=RED)
        score_pushed = Text("-0.45", font_size=32, color=YELLOW).next_to(sim_text, RIGHT)
        
        self.play(
            Transform(txt_in_correct, txt_in_wrong),
            Transform(v_txt, pushed_v_txt),
            v_txt_label.animate.next_to(pushed_v_txt.get_end(), DL, buff=0.1),
            Transform(score, score_pushed),
            run_time=2
        )
        
        # 8. Formula Display
        formula = MathTex(
            r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})", 
            font_size=36
        ).to_edge(DOWN, buff=1)
        self.play(Write(formula))
        
        self.wait(2)