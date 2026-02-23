from manim import *
import numpy as np

class ContrastiveAlignment(Scene):
    def construct(self):
        # 1. Formula Display
        formula = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})", font_size=32)
        formula.to_edge(UP)
        self.add(formula)

        # 2. Encoders Setup
        image_encoder_rect = Rectangle(width=2.5, height=1.5, color=BLUE).shift(LEFT * 4 + UP * 1.5)
        image_encoder_label = Text("Image Encoder", font_size=20).move_to(image_encoder_rect)
        
        text_encoder_rect = Rectangle(width=2.5, height=1.5, color=GREEN).shift(LEFT * 4 + DOWN * 1.5)
        text_encoder_label = Text("Text Encoder", font_size=20).move_to(text_encoder_rect)

        # 3. Inputs
        # Try to load the image, otherwise use a placeholder box
        try:
            street_view_img = ImageMobject("img-7.jpeg").scale(0.4).next_to(image_encoder_rect, LEFT, buff=0.5)
        except:
            street_view_img = Rectangle(width=1.5, height=1.2, color=BLUE, fill_opacity=0.3).next_to(image_encoder_rect, LEFT, buff=0.5)
            street_view_img.add(Text("Image", font_size=14).move_to(street_view_img))

        caption_france = Text("A Street View photo in France", font_size=18, color=GREEN).next_to(text_encoder_rect, LEFT, buff=0.4)
        caption_japan = Text("A Street View photo in Japan", font_size=18, color=RED).next_to(text_encoder_rect, LEFT, buff=0.4)

        # 4. Manual Embedding Space (Replacing Axes which was disallowed)
        axis_x = Line(LEFT * 2, RIGHT * 2, color=WHITE).shift(RIGHT * 3.5)
        axis_y = Line(DOWN * 2, UP * 2, color=WHITE).shift(RIGHT * 3.5)
        origin = axis_x.get_center()
        space_title = Text("Shared Embedding Space", font_size=16).next_to(axis_y, UP)

        # 5. Vectors
        # Start vectors at different positions
        v_img = Arrow(origin, origin + [1.0, 1.2, 0], buff=0, color=BLUE)
        v_txt = Arrow(origin, origin + [-1.2, 0.5, 0], buff=0, color=GREEN)
        
        # Labels for vectors
        label_v_img = MathTex(r"v_{img}", color=BLUE, font_size=24)
        label_v_txt = MathTex(r"v_{text}", color=GREEN, font_size=24)

        # 6. Similarity Score (Replacing DecimalNumber which was disallowed)
        sim_label = Text("Similarity Score:", font_size=22).shift(DOWN * 3 + RIGHT * 2.5)
        sim_val = Text("0.12", font_size=22).next_to(sim_label, RIGHT)

        # Animation Sequence
        self.play(
            Create(image_encoder_rect), Write(image_encoder_label),
            Create(text_encoder_rect), Write(text_encoder_label),
            Create(axis_x), Create(axis_y), Write(space_title)
        )
        self.wait(0.5)

        # Inputs enter encoders
        self.play(FadeIn(street_view_img, shift=RIGHT), Write(caption_france))
        self.play(Create(v_img), Create(v_txt))
        self.play(Write(sim_label), Write(sim_val))
        self.wait(1)

        # Align vectors (Correct association)
        # We define a target point in the space
        target_point = origin + [1.5, 0.8, 0]
        
        # Updating the score manually as we animate
        self.play(
            v_img.animate.put_start_and_end_on(origin, target_point),
            v_txt.animate.put_start_and_end_on(origin, target_point),
            sim_val.animate.become(Text("0.99", font_size=22, color=YELLOW).next_to(sim_label, RIGHT)),
            run_time=2
        )
        self.wait(1)

        # Contrastive step: Change text to "Japan"
        self.play(
            FadeOut(caption_france, shift=DOWN),
            FadeIn(caption_japan, shift=UP)
        )
        self.wait(0.5)

        # Push vector away (Incorrect association)
        away_point = origin + [-1.2, -0.8, 0]
        self.play(
            v_txt.animate.put_start_and_end_on(origin, away_point).set_color(RED),
            sim_val.animate.become(Text("-0.85", font_size=22, color=RED).next_to(sim_label, RIGHT)),
            run_time=2
        )
        
        self.wait(2)