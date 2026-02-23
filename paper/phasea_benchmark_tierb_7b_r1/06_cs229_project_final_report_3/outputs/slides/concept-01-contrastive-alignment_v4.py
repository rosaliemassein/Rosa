from manim import *

class ContrastiveAlignment(Scene):
    def construct(self):
        # 1. Setup Title and Formula
        title = Text("Contrastive Alignment in CLIP", font_size=32).to_edge(UP)
        formula = MathTex(
            r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})",
            font_size=24
        ).to_edge(DL)
        
        self.add(title)
        self.play(Write(formula))

        # 2. Neural network blocks (Encoders)
        img_enc_box = Rectangle(width=2.8, height=1.2, color=BLUE)
        img_enc_label = Text("Image Encoder", font_size=20)
        img_encoder = VGroup(img_enc_box, img_enc_label).shift(UP * 1.5 + LEFT * 3.5)
        
        txt_enc_box = Rectangle(width=2.8, height=1.2, color=RED)
        txt_enc_label = Text("Text Encoder", font_size=20)
        txt_encoder = VGroup(txt_enc_box, txt_enc_label).shift(DOWN * 1.5 + LEFT * 3.5)

        self.play(Create(img_encoder), Create(txt_encoder))

        # 3. Inputs: Street View Image and Text Label
        # Using a rectangle with a small internal label as a placeholder for the image
        img_in_box = Rectangle(width=1.5, height=1.0, color=WHITE).set_fill(GRAY, opacity=0.5)
        img_in_label = Text("Street View", font_size=14)
        img_input = VGroup(img_in_box, img_in_label).next_to(img_encoder, LEFT, buff=1)
        
        text_input_france = Text("'A photo in France'", font_size=18, color=YELLOW).next_to(txt_encoder, LEFT, buff=1)
        
        self.play(FadeIn(img_input), FadeIn(text_input_france))
        self.wait(0.5)

        # 4. Shared Embedding Space (Manual Axes using Line)
        origin_point = RIGHT * 3
        axis_x = Line(origin_point + LEFT * 1.5, origin_point + RIGHT * 2, color=WHITE)
        axis_y = Line(origin_point + DOWN * 1.5, origin_point + UP * 2, color=WHITE)
        space_label = Text("Shared Embedding Space", font_size=16).next_to(axis_y, UP)
        
        self.play(Create(axis_x), Create(axis_y), Write(space_label))

        # 5. Vectors (Using Arrow instead of Vector)
        # Image vector (fixed)
        v_img = Arrow(origin_point, origin_point + RIGHT * 1.5 + UP * 1.5, buff=0, color=BLUE)
        # Text vector (initially misaligned)
        v_txt = Arrow(origin_point, origin_point + LEFT * 0.5 + UP * 1.8, buff=0, color=RED)
        
        # Animate inputs moving into encoders and appearing as vectors
        self.play(
            img_input.animate.scale(0.1).move_to(img_encoder.get_center()).set_opacity(0),
            text_input_france.animate.scale(0.1).move_to(txt_encoder.get_center()).set_opacity(0),
            GrowArrow(v_img),
            GrowArrow(v_txt),
            run_time=2
        )

        # 6. Similarity Score (Using Text instead of DecimalNumber/ValueTracker)
        sim_text_start = Text("Cosine Similarity: 0.45", font_size=22, color=WHITE).shift(RIGHT * 3 + DOWN * 2.2)
        self.play(Write(sim_text_start))
        self.wait(1)

        # 7. Alignment (Maximizing similarity for correct label)
        v_txt_aligned = Arrow(origin_point, origin_point + RIGHT * 1.6 + UP * 1.6, buff=0, color=RED)
        sim_text_high = Text("Cosine Similarity: 0.98", font_size=22, color=GREEN).move_to(sim_text_start)
        
        self.play(
            Transform(v_txt, v_txt_aligned),
            Transform(sim_text_start, sim_text_high),
            run_time=2
        )
        self.wait(1)

        # 8. Contrastive Step: Show "Japan" label being pushed away
        text_input_japan = Text("'A photo in Japan'", font_size=18, color=ORANGE).next_to(txt_encoder, LEFT, buff=1)
        self.play(FadeIn(text_input_japan))
        
        v_txt_wrong = Arrow(origin_point, origin_point + RIGHT * 1.8 + DOWN * 1.0, buff=0, color=RED)
        sim_text_low = Text("Cosine Similarity: 0.12", font_size=22, color=RED).move_to(sim_text_start)

        self.play(
            text_input_japan.animate.scale(0.1).move_to(txt_encoder.get_center()).set_opacity(0),
            Transform(v_txt, v_txt_wrong),
            Transform(sim_text_start, sim_text_low),
            run_time=2
        )
        
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(VGroup(title, formula, img_encoder, txt_encoder, axis_x, axis_y, space_label, v_img, v_txt, sim_text_start)))