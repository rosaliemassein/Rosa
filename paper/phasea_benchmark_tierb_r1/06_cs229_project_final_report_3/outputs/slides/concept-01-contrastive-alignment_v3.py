from manim import *

class Concept01ContrastiveAlignment(Scene):
    def construct(self):
        # 1. Setup Neural Network Blocks (Encoders)
        img_rect = Rectangle(width=3, height=1.5, color=WHITE)
        img_text = Text("Image Encoder", font_size=24)
        img_encoder = VGroup(img_rect, img_text).shift(LEFT * 4 + UP * 2.5)

        txt_rect = Rectangle(width=3, height=1.5, color=WHITE)
        txt_text = Text("Text Encoder", font_size=24)
        txt_encoder = VGroup(txt_rect, txt_text).shift(RIGHT * 4 + UP * 2.5)

        self.add(img_encoder, txt_encoder)

        # 2. Inputs
        input_image = Square(side_length=0.8, fill_opacity=0.8, fill_color=YELLOW).next_to(img_encoder, UP, buff=0.5)
        input_text_france = Text("'A photo in France'", font_size=20, color=BLUE).next_to(txt_encoder, UP, buff=0.5)

        self.play(FadeIn(input_image), FadeIn(input_text_france))
        self.play(
            input_image.animate.scale(0.2).move_to(img_encoder.get_center()),
            input_text_france.animate.scale(0.5).move_to(txt_encoder.get_center()),
        )

        # 3. Embedding Space (Manual Axes)
        origin = DOWN * 1.5
        x_axis = Arrow(origin + LEFT * 2.5, origin + RIGHT * 2.5, buff=0, color=GREY_B)
        y_axis = Arrow(origin + DOWN * 0.5, origin + UP * 2.5, buff=0, color=GREY_B)
        space_label = Text("Shared Embedding Space", font_size=20).next_to(y_axis, UP)
        self.play(Create(x_axis), Create(y_axis), Write(space_label))

        # 4. Vectors
        v_img = Arrow(origin, origin + UP * 1.5 + RIGHT * 1.0, buff=0, color=YELLOW)
        v_txt = Arrow(origin, origin + UP * 1.8 + LEFT * 0.8, buff=0, color=BLUE)
        v_img_label = Text("Image", font_size=16, color=YELLOW).next_to(v_img.get_end(), RIGHT)
        v_txt_label = Text("Text (FR)", font_size=16, color=BLUE).next_to(v_txt.get_end(), LEFT)

        self.play(GrowArrow(v_img), GrowArrow(v_txt))
        self.play(Write(v_img_label), Write(v_txt_label))

        # 5. Similarity Score (Using Text instead of DecimalNumber/ValueTracker)
        score_title = Text("Cosine Similarity:", font_size=24).to_edge(RIGHT).shift(UP * 0.5)
        score_val = Text("0.32", font_size=24).next_to(score_title, RIGHT)
        self.add(score_title, score_val)

        # 6. Alignment Animation
        target_end = origin + UP * 1.6 + RIGHT * 1.6
        score_high = Text("0.98", font_size=24, color=GREEN).move_to(score_val)
        
        self.play(
            v_img.animate.put_start_and_end_on(origin, target_end),
            v_txt.animate.put_start_and_end_on(origin, target_end + RIGHT * 0.1),
            v_img_label.animate.move_to(target_end + RIGHT * 0.5 + UP * 0.2),
            v_txt_label.animate.move_to(target_end + RIGHT * 0.5 + DOWN * 0.2),
            Transform(score_val, score_high),
            run_time=2
        )
        self.wait(1)

        # 7. Wrong label (Japan)
        input_text_japan = Text("'A photo in Japan'", font_size=10, color=RED).move_to(txt_encoder.get_center())
        v_txt_wrong_end = origin + UP * 0.2 + LEFT * 1.8
        v_txt_lab_jp = Text("Text (JP)", font_size=16, color=RED).next_to(v_txt_wrong_end, LEFT)
        score_low = Text("-0.15", font_size=24, color=RED).move_to(score_val)

        self.play(
            FadeOut(input_text_france),
            FadeIn(input_text_japan),
            Transform(v_txt, Arrow(origin, v_txt_wrong_end, buff=0, color=RED)),
            Transform(v_txt_label, v_txt_lab_jp),
            Transform(score_val, score_low),
            run_time=2
        )
        self.wait(1)

        # 8. Formula
        formula = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})", font_size=36)
        formula.to_edge(LEFT).shift(UP * 0.5)
        self.play(Write(formula))
        self.wait(2)