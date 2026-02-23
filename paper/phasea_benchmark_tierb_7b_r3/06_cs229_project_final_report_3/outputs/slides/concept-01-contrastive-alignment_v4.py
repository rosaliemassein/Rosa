from manim import *

class ContrastiveAlignmentScene(Scene):
    def construct(self):
        # 1. Setup layout elements
        title = Text("Contrastive Learning Alignment", font_size=32).to_edge(UP)
        
        # Encoders as simple geometric groups
        img_enc_rect = Rectangle(width=2.5, height=1.5, color=BLUE)
        img_enc_text = Text("Image Encoder", font_size=20)
        img_encoder = VGroup(img_enc_rect, img_enc_text).shift(LEFT * 4 + UP * 1)
        
        txt_enc_rect = Rectangle(width=2.5, height=1.5, color=GREEN)
        txt_enc_text = Text("Text Encoder", font_size=20)
        txt_encoder = VGroup(txt_enc_rect, txt_enc_text).shift(RIGHT * 4 + UP * 1)
        
        # Inputs to the encoders
        img_in = Square(side_length=0.8, color=YELLOW).next_to(img_encoder, LEFT, buff=0.5)
        txt_in = Text("'A photo in France'", font_size=18).next_to(txt_encoder, RIGHT, buff=0.5)
        
        # 2. Embedding Space (Manual creation to avoid Axes identifier issues)
        # Using simple Lines and Arrows
        x_axis_line = Line(LEFT * 2.5, RIGHT * 2.5, color=GRAY)
        y_axis_line = Line(DOWN * 2, UP * 1, color=GRAY)
        space_origin = [0, -1.5, 0] # Define a center for the coordinate system
        
        coordinate_system = VGroup(x_axis_line, y_axis_line).move_to(space_origin)
        space_label = Text("Shared Embedding Space", font_size=20).next_to(coordinate_system, UP, buff=0.3)
        
        # Initial Vectors (Image and Text)
        # Starting points at space_origin
        vec_img = Arrow(space_origin, space_origin + [1.5, 0.7, 0], color=BLUE, buff=0)
        vec_txt = Arrow(space_origin, space_origin + [-0.5, 1.2, 0], color=GREEN, buff=0)
        
        img_label = MathTex("v_{img}", color=BLUE, font_size=24).next_to(vec_img.get_end(), RIGHT, buff=0.1)
        txt_label = MathTex("v_{text}", color=GREEN, font_size=24).next_to(vec_txt.get_end(), LEFT, buff=0.1)
        
        # 3. Text-based Similarity Score
        sim_score = Text("Cosine Similarity: 0.12", font_size=26, color=YELLOW).to_edge(DOWN, buff=1.2)

        # --- ANIMATION SEQUENCE ---
        
        # Introduction
        self.play(Write(title))
        self.play(Create(img_encoder), Create(txt_encoder))
        self.play(FadeIn(img_in), FadeIn(txt_in))
        self.wait(0.5)
        
        # Showing the shared space and initial embeddings
        self.play(Create(coordinate_system), Write(space_label))
        self.play(
            GrowArrow(vec_img), 
            GrowArrow(vec_txt), 
            Write(img_label), 
            Write(txt_label)
        )
        self.play(Write(sim_score))
        self.wait(1)
        
        # Step 1: Maximize similarity (France image + France text)
        # Transform the text vector to point in the same direction as the image vector
        vec_txt_aligned = Arrow(space_origin, space_origin + [1.6, 0.75, 0], color=GREEN, buff=0)
        txt_label_aligned = MathTex("v_{text}", color=GREEN, font_size=24).next_to(vec_txt_aligned.get_end(), UP, buff=0.1)
        sim_score_high = Text("Cosine Similarity: 0.98", font_size=26, color=YELLOW).to_edge(DOWN, buff=1.2)
        
        self.play(
            Transform(vec_txt, vec_txt_aligned),
            Transform(txt_label, txt_label_aligned),
            Transform(sim_score, sim_score_high),
            run_time=2
        )
        self.wait(1)
        
        # Step 2: Contrast with "wrong" label (Japan)
        txt_in_wrong = Text("'A photo in Japan'", font_size=18, color=RED).move_to(txt_in)
        self.play(Transform(txt_in, txt_in_wrong))
        
        # Pushing away (Contrastive step)
        vec_txt_away = Arrow(space_origin, space_origin + [-1.5, -0.8, 0], color=RED, buff=0)
        txt_label_away = MathTex("v_{text}", color=RED, font_size=24).next_to(vec_txt_away.get_end(), LEFT, buff=0.1)
        sim_score_low = Text("Cosine Similarity: -0.34", font_size=26, color=YELLOW).to_edge(DOWN, buff=1.2)
        
        self.play(
            Transform(vec_txt, vec_txt_away),
            Transform(txt_label, txt_label_away),
            Transform(sim_score, sim_score_low),
            run_time=2
        )
        self.wait(1)
        
        # Final: Display the CLIP Loss formula
        formula = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})", font_size=34)
        formula.to_edge(DOWN, buff=0.5)
        
        self.play(FadeOut(sim_score))
        self.play(Write(formula))
        self.play(Indicate(formula, color=YELLOW))
        
        self.wait(2)