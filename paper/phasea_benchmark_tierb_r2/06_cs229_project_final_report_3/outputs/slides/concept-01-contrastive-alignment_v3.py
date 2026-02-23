from manim import *

class Concept01ContrastiveAlignment(Scene):
    def construct(self):
        # 1. Narration Text
        narration = Text(
            "Aligning visual features with geographic concepts in a shared space.",
            font_size=24
        ).to_edge(DOWN)
        self.add(narration)

        # 2. Encoders
        img_box = Rectangle(color=BLUE, height=1.2, width=2.5).shift(LEFT * 3 + UP * 2)
        img_lab = Text("Image Encoder", font_size=20).move_to(img_box)
        txt_box = Rectangle(color=GREEN, height=1.2, width=2.5).shift(RIGHT * 3 + UP * 2)
        txt_lab = Text("Text Encoder", font_size=20).move_to(txt_box)
        
        self.play(Create(img_box), Create(img_lab), Create(txt_box), Create(txt_lab))

        # 3. Input Animation
        # Use Square as a placeholder for the street view image
        img_input = Square(color=BLUE, side_length=0.8).next_to(img_box, LEFT, buff=0.8)
        img_input_lab = Text("Image", font_size=14).move_to(img_input)
        txt_input = Text("'Street in France'", font_size=18).next_to(txt_box, RIGHT, buff=0.8)
        
        self.play(FadeIn(img_input), FadeIn(img_input_lab), Write(txt_input))
        self.play(
            img_input.animate.move_to(img_box).scale(0.2),
            img_input_lab.animate.move_to(img_box).scale(0.2),
            txt_input.animate.move_to(txt_box).scale(0.5)
        )
        self.play(FadeOut(img_input), FadeOut(img_input_lab), FadeOut(txt_input))

        # 4. Shared Embedding Space (Manual Coordinate System)
        # Using DOWN as the base point to avoid numpy 'np' usage
        base_point = DOWN
        xaxis = Line(base_point + LEFT*2, base_point + RIGHT*2, color=WHITE)
        yaxis = Line(base_point + DOWN*0.5, base_point + UP*1.8, color=WHITE)
        space_lab = Text("Shared Embedding Space", font_size=16).next_to(yaxis, UP)
        self.play(Create(xaxis), Create(yaxis), Write(space_lab))

        # 5. Vectors Alignment (France)
        # Image Vector (Blue)
        v_img = Arrow(base_point, base_point + RIGHT*1.2 + UP*1.2, buff=0, color=BLUE)
        # Text Vector (Green) - initially misaligned
        v_txt = Arrow(base_point, base_point + LEFT*0.8 + UP*1.4, buff=0, color=GREEN)
        
        self.play(Create(v_img), Create(v_txt))
        
        # Similarity Text (using Transform instead of ValueTracker)
        sim_text = Text("Similarity: 0.12", font_size=22, color=YELLOW).shift(RIGHT * 3.5 + DOWN * 1)
        self.play(Write(sim_text))
        self.wait(0.5)

        # Animate alignment
        v_txt_aligned = Arrow(base_point, base_point + RIGHT*1.2 + UP*1.2, buff=0, color=GREEN)
        sim_text_high = Text("Similarity: 0.99", font_size=22, color=YELLOW).move_to(sim_text)
        
        self.play(
            Transform(v_txt, v_txt_aligned),
            Transform(sim_text, sim_text_high),
            run_time=2
        )
        self.wait(1)

        # 6. Contrastive Pushing (Japan)
        # New text input
        wrong_label = Text("'Street in Japan'", font_size=18, color=RED).move_to(txt_box)
        self.play(FadeIn(wrong_label, shift=UP))
        
        # Red vector pushed away
        v_txt_wrong = Arrow(base_point, base_point + LEFT*1.5 + DOWN*0.2, buff=0, color=RED)
        sim_text_low = Text("Similarity: -0.45", font_size=22, color=YELLOW).move_to(sim_text)
        
        self.play(
            Transform(v_txt, v_txt_wrong),
            Transform(sim_text, sim_text_low),
            run_time=2
        )
        self.wait(1)

        # 7. Final Formula
        formula = MathTex(r"\mathcal{L}_{CLIP} = 0.5 \cdot (\mathcal{L}_{Text} + \mathcal{L}_{Images})")
        formula.scale(0.8).to_edge(UP, buff=0.4)
        self.play(Write(formula))
        self.wait(2)