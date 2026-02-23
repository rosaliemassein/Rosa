from manim import *

class ContrastiveAlignment(Scene):
    def construct(self):
        # 1. Encoders and UI
        img_box = Rectangle(width=3, height=1, color=BLUE).shift(LEFT * 3 + UP * 2.5)
        img_txt = Text("Image Encoder", font_size=20).move_to(img_box)
        image_encoder = VGroup(img_box, img_txt)

        txt_box = Rectangle(width=3, height=1, color=RED).shift(RIGHT * 3 + UP * 2.5)
        txt_txt = Text("Text Encoder", font_size=20).move_to(txt_box)
        text_encoder = VGroup(txt_box, txt_txt)

        france_label = Text("A photo in France", font_size=18, color=YELLOW).next_to(txt_box, UP)
        japan_label = Text("A photo in Japan", font_size=18, color=RED).next_to(txt_box, UP)
        formula = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})", font_size=28).to_corner(UR)

        # 2. Manual Coordinate System
        origin_pt = DOWN * 1.5 + LEFT * 0.5
        x_line = Line(origin_pt, origin_pt + RIGHT * 3, color=WHITE)
        y_line = Line(origin_pt, origin_pt + UP * 3, color=WHITE)
        x_line.add_tip()
        y_line.add_tip()
        space_label = Text("Embedding Space", font_size=16).next_to(y_line, UP)
        space = VGroup(x_line, y_line, space_label)

        # Vectors
        img_vec = Arrow(origin_pt, origin_pt + [1.8, 1.8, 0], color=BLUE, buff=0)
        txt_vec = Arrow(origin_pt, origin_pt + [2.2, 0.4, 0], color=YELLOW, buff=0)
        img_tag = Text("Image", font_size=14, color=BLUE).next_to(img_vec.get_end(), UR, buff=0.1)
        txt_tag = Text("Text", font_size=14, color=YELLOW).next_to(txt_vec.get_end(), RIGHT, buff=0.1)

        # Similarity Scores
        sim_title = Text("Similarity: ", font_size=24).to_corner(UL).shift(DOWN * 0.5)
        score_1 = Text("0.12", font_size=24, color=WHITE).next_to(sim_title, RIGHT)
        score_2 = Text("0.95", font_size=24, color=GREEN).next_to(sim_title, RIGHT)
        score_3 = Text("-0.42", font_size=24, color=RED).next_to(sim_title, RIGHT)

        # 3. Animation Steps
        self.add(image_encoder, text_encoder, formula)
        
        # Display street view photo (placeholder handled by Manim if image missing)
        try:
            street_img = ImageMobject("img-7.jpeg").scale(0.4).next_to(image_encoder, LEFT)
            self.add(street_img)
        except:
            street_img = Square(side_length=1, color=GRAY).next_to(image_encoder, LEFT)
            self.add(street_img)

        self.play(Write(france_label))
        self.play(Create(space))
        self.play(GrowArrow(img_vec), Write(img_tag))
        self.play(GrowArrow(txt_vec), Write(txt_tag))
        self.add(sim_title, score_1)
        self.wait(1)

        # Step 1: Alignment (Positive Pair)
        new_txt_end = origin_pt + [1.7, 1.7, 0]
        self.play(
            txt_vec.animate.put_start_and_end_on(origin_pt, new_txt_end),
            txt_tag.animate.move_to(origin_pt + [2.1, 1.7, 0]),
            ReplacementTransform(score_1, score_2),
            run_time=2
        )
        self.play(Indicate(score_2))
        self.wait(1)

        # Step 2: Push Away (Negative Pair)
        self.play(ReplacementTransform(france_label, japan_label))
        pushed_txt_end = origin_pt + [2.0, -1.0, 0]
        self.play(
            txt_vec.animate.put_start_and_end_on(origin_pt, pushed_txt_end),
            txt_tag.animate.move_to(origin_pt + [2.4, -1.0, 0]),
            ReplacementTransform(score_2, score_3),
            run_time=2
        )
        self.play(Indicate(score_3))
        self.wait(2)