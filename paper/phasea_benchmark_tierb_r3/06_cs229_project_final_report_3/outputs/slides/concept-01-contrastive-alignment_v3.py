from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Background Formula
        formula = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})", font_size=30)
        formula.to_edge(DOWN, buff=0.5)
        self.add(formula)

        # 2. Encoders
        img_enc_rect = Rectangle(height=1.0, width=2.5, color=BLUE)
        img_enc_text = Text("Image Encoder", font_size=20)
        img_enc = VGroup(img_enc_rect, img_enc_text).shift(LEFT * 4 + UP * 2)

        txt_enc_rect = Rectangle(height=1.0, width=2.5, color=GREEN)
        txt_enc_text = Text("Text Encoder", font_size=20)
        txt_enc = VGroup(txt_enc_rect, txt_enc_text).shift(LEFT * 4 + DOWN * 0.5)

        self.play(Create(img_enc), Create(txt_enc))

        # 3. Inputs
        img_input = Square(side_length=0.8, color=WHITE).next_to(img_enc, LEFT, buff=0.5)
        img_input_label = Text("Image", font_size=14).move_to(img_input)
        
        caption_france = Text("A Street View photo in France", font_size=16, color=YELLOW).next_to(txt_enc, LEFT, buff=0.2)
        caption_japan = Text("A Street View photo in Japan", font_size=16, color=RED).move_to(caption_france)

        self.play(FadeIn(img_input), FadeIn(img_input_label), Write(caption_france))
        self.wait(1)

        # 4. Shared Embedding Space (Simplified Axes)
        origin = RIGHT * 2 + DOWN * 1
        x_axis = Line(origin, origin + RIGHT * 3, color=GREY_A)
        y_axis = Line(origin, origin + UP * 3, color=GREY_A)
        space_label = Text("Shared Embedding Space", font_size=20).next_to(y_axis, UP)
        
        self.play(Create(x_axis), Create(y_axis), Write(space_label))

        # 5. Vectors and Similarity Score
        # Image vector (fixed)
        target_pos = origin + RIGHT * 2.5 + UP * 1.5
        v_img = Arrow(origin, target_pos, buff=0, color=BLUE)
        v_img_label = Text("Image Vector", font_size=14, color=BLUE).next_to(v_img.get_end(), UP, buff=0.1)

        # Text vector (starts unaligned)
        start_txt_pos = origin + RIGHT * 0.5 + UP * 2.5
        v_txt = Arrow(origin, start_txt_pos, buff=0, color=YELLOW)
        v_txt_label = Text("Text Vector", font_size=14, color=YELLOW).next_to(v_txt.get_end(), RIGHT, buff=0.1)

        # Similarity Text
        sim_score_label = Text("Cosine Similarity:", font_size=18).shift(RIGHT * 3.5 + DOWN * 2)
        sim_val_low = Text("0.42", font_size=18).next_to(sim_score_label, RIGHT)
        sim_val_high = Text("0.98", font_size=18, color=GREEN).next_to(sim_score_label, RIGHT)
        sim_val_wrong = Text("0.11", font_size=18, color=RED).next_to(sim_score_label, RIGHT)

        self.play(GrowArrow(v_img), FadeIn(v_img_label))
        self.play(GrowArrow(v_txt), FadeIn(v_txt_label))
        self.play(Write(sim_score_label), FadeIn(sim_val_low))
        self.wait(1)

        # 6. Alignment Animation (Positive Pair)
        aligned_pos = origin + RIGHT * 2.4 + UP * 1.45 # Near identical to image vector
        self.play(
            v_txt.animate.put_start_and_end_on(origin, aligned_pos),
            v_txt_label.animate.next_to(aligned_pos, DOWN, buff=0.1),
            Transform(sim_val_low, sim_val_high),
            run_time=2
        )
        self.wait(1)

        # 7. Push Away Animation (Negative Pair)
        self.play(
            Transform(caption_france, caption_japan),
            v_txt.animate.set_color(RED),
            v_txt_label.animate.set_color(RED)
        )
        
        pushed_pos = origin + RIGHT * 2.8 + UP * 0.3 # Pushed towards X axis
        self.play(
            v_txt.animate.put_start_and_end_on(origin, pushed_pos),
            v_txt_label.animate.next_to(pushed_pos, UP, buff=0.1),
            Transform(sim_val_low, sim_val_wrong),
            run_time=2
        )
        self.wait(2)

        # Conclusion Text
        conclusion = Text("Aligning images with geography concepts", font_size=22).to_edge(UP)
        self.play(Write(conclusion))
        self.wait(2)