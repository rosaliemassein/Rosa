from manim import *

class ConceptAnimation01(Scene):
    def construct(self):
        # 1. Encoders (Image and Text Blocks)
        img_box = RoundedRectangle(height=1, width=2.2, color=BLUE).shift(UP * 2.5 + LEFT * 3)
        img_text = Text("Image Encoder", font_size=20).move_to(img_box)
        
        txt_box = RoundedRectangle(height=1, width=2.2, color=GREEN).shift(UP * 2.5 + RIGHT * 3)
        txt_text = Text("Text Encoder", font_size=20).move_to(txt_box)
        
        self.add(img_box, img_text, txt_box, txt_text)
        
        # 2. Inputs
        img_in = Square(side_length=0.8, color=WHITE).next_to(img_box, LEFT, buff=0.4)
        img_in_label = Text("Image", font_size=14).move_to(img_in)
        txt_in = Text("'A Street View photo in France'", font_size=16).next_to(txt_box, RIGHT, buff=0.4)
        
        self.play(FadeIn(img_in), FadeIn(img_in_label), Write(txt_in))
        self.wait(0.5)
        
        # 3. Shared Embedding Space (Manual Coordinate System)
        # Using simple Arrows instead of Axes to avoid "disallowed" identifiers
        origin_pt = DOWN * 1.5 + LEFT * 1.5
        x_axis = Arrow(origin_pt, origin_pt + RIGHT * 4, buff=0, color=WHITE)
        y_axis = Arrow(origin_pt, origin_pt + UP * 3, buff=0, color=WHITE)
        space_label = Text("Shared Embedding Space", font_size=18).next_to(x_axis, DOWN, buff=0.3)
        
        self.play(Create(x_axis), Create(y_axis), Write(space_label))
        
        # 4. Vectors (Image and Text)
        # Initial separate directions
        vec_img = Arrow(origin_pt, origin_pt + [1, 2, 0], buff=0, color=BLUE)
        vec_txt = Arrow(origin_pt, origin_pt + [2.5, 0.5, 0], buff=0, color=GREEN)
        
        img_label = Text("Image Vec", font_size=14, color=BLUE).next_to(vec_img.get_end(), UP)
        txt_label = Text("France Vec", font_size=14, color=GREEN).next_to(vec_txt.get_end(), RIGHT)
        
        self.play(GrowArrow(vec_img), GrowArrow(vec_txt), Write(img_label), Write(txt_label))
        
        # 5. Similarity Score (Manual updates)
        sim_title = Text("Cosine Similarity: ", font_size=24).to_edge(UP, buff=0.7)
        sim_val = Text("0.35", font_size=24, color=YELLOW).next_to(sim_title, RIGHT)
        self.play(Write(sim_title), Write(sim_val))
        
        # 6. Animate Alignment (Positive Pair)
        target_pt = origin_pt + [2, 2, 0]
        sim_val_aligned = Text("1.00", font_size=24, color=YELLOW).move_to(sim_val)
        
        self.play(
            vec_img.animate.put_start_and_end_on(origin_pt, target_pt),
            vec_txt.animate.put_start_and_end_on(origin_pt, target_pt),
            img_label.animate.move_to(origin_pt + [1.8, 2.3, 0]),
            txt_label.animate.move_to(origin_pt + [2.3, 1.8, 0]),
            ReplacementTransform(sim_val, sim_val_aligned),
            run_time=2
        )
        self.wait(1)
        
        # 7. Wrong Label (Negative Pair)
        txt_wrong = Text("'A Street View photo in Japan'", font_size=16, color=RED).move_to(txt_in)
        self.play(ReplacementTransform(txt_in, txt_wrong))
        
        # Create Japan vector starting near the image
        vec_japan = Arrow(origin_pt, target_pt, buff=0, color=RED)
        japan_label = Text("Japan Vec", font_size=14, color=RED).move_to(txt_label)
        
        self.play(FadeOut(vec_txt), FadeOut(txt_label))
        self.play(FadeIn(vec_japan), Write(japan_label))
        
        # Pushing away (Contrastive Learning)
        away_pt = origin_pt + [3.5, 0.3, 0]
        sim_val_low = Text("0.12", font_size=24, color=YELLOW).move_to(sim_val_aligned)
        
        self.play(
            vec_japan.animate.put_start_and_end_on(origin_pt, away_pt),
            japan_label.animate.next_to(away_pt, RIGHT),
            ReplacementTransform(sim_val_aligned, sim_val_low),
            run_time=2
        )
        self.wait(1)
        
        # 8. Show Formula
        formula = MathTex(
            r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})",
            color=WHITE
        ).scale(0.8).to_edge(DOWN, buff=0.2)
        
        self.play(Write(formula))
        self.wait(3)