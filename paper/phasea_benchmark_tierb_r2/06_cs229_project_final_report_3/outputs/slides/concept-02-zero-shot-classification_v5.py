from manim import *

class ZeroShotClassification(Scene):
    def construct(self):
        # 1. Image Representation
        # Use a placeholder if the image file is missing to ensure compilation
        try:
            image = ImageMobject("img-8.jpeg").scale(0.6).to_edge(UL, buff=0.5)
        except:
            image = Rectangle(height=2, width=3, color=BLUE).to_edge(UL, buff=0.5)
            image.add(Text("Input Image", font_size=20).move_to(image))
        
        image_label = Text("Image Input", font_size=20).next_to(image, UP)
        self.play(FadeIn(image), Write(image_label))

        # 2. Vector v (Manual construction to avoid Matrix identifier issues)
        v_bracket_l = MathTex(r"[").scale(2)
        v_content = MathTex(r"v_1 \\ v_2 \\ \vdots \\ v_d").scale(0.8)
        v_bracket_r = MathTex(r"]").scale(2)
        v_group = VGroup(v_bracket_l, v_content, v_bracket_r).arrange(RIGHT, buff=0.1)
        v_label = MathTex(r"\mathbf{v}").next_to(v_group, UP)
        v_full = VGroup(v_label, v_group).scale(0.7).next_to(image, RIGHT, buff=1)

        self.play(Write(v_label), Create(v_group))
        self.wait()

        # 3. Matrix X (Manual construction for country list)
        countries = ["USA", "Canada", "France", "Japan", "Brazil"]
        x_rows = VGroup(*[Text(name, font_size=24) for name in countries]).arrange(DOWN, buff=0.4)
        x_bracket_l = MathTex(r"[").scale(4).next_to(x_rows, LEFT)
        x_bracket_r = MathTex(r"]").scale(4).next_to(x_rows, RIGHT)
        x_matrix = VGroup(x_bracket_l, x_rows, x_bracket_r).scale(0.7).to_edge(RIGHT, buff=1)
        x_label = MathTex(r"\mathbf{X}").next_to(x_matrix, UP)

        self.play(Write(x_label), Create(x_matrix))
        self.wait()

        # 4. Dot Product Animation
        highlight_box = Rectangle(width=2, height=0.5, color=YELLOW).move_to(x_rows[0])
        dot_text = Text("Dot Product: Xv", font_size=24, color=YELLOW).to_edge(UP)
        
        self.play(Write(dot_text))
        for i in range(len(countries)):
            self.play(highlight_box.animate.move_to(x_rows[i]), run_time=0.3)
            self.play(Indicate(v_group), run_time=0.3)
        
        self.play(FadeOut(highlight_box), FadeOut(dot_text))

        # 5. Bar Chart (Manual construction using Rectangles)
        chart_base = Line(LEFT * 2.5, RIGHT * 2.5).shift(DOWN * 2)
        bars = VGroup(*[
            Rectangle(width=0.5, height=0.1, color=BLUE, fill_opacity=0.8) 
            for _ in range(len(countries))
        ]).arrange(RIGHT, buff=0.4).shift(DOWN * 2)
        
        # Align bars to the bottom line
        for bar in bars:
            bar.align_to(chart_base, DOWN)

        bar_labels = VGroup(*[
            Text(countries[i], font_size=14).next_to(bars[i], DOWN)
            for i in range(len(countries))
        ])

        softmax_title = Text("Softmax Probabilities", font_size=24).next_to(bars, UP, buff=1)

        self.play(Create(chart_base), Create(bars), Write(bar_labels), Write(softmax_title))
        self.wait()

        # Target heights for Softmax (France is index 2)
        target_heights = [0.2, 0.4, 2.5, 0.3, 0.2]
        
        # Animate bars growing
        animations = []
        for i in range(len(bars)):
            animations.append(bars[i].animate.set_height(target_heights[i], stretch=True).move_to(bars[i].get_bottom(), aligned_edge=DOWN))
        
        self.play(*animations, bars[2].animate.set_color(GREEN), run_time=1.5)
        self.wait()

        # 6. Final formula
        formula = MathTex(
            r"h(\mathbf{v};\mathbf{X})=\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}"
        ).scale(0.8).to_edge(DL, buff=0.5)
        
        # Solid background for formula using a Rectangle
        formula_bg = Rectangle(
            width=formula.get_width() + 0.4,
            height=formula.get_height() + 0.4,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=0
        ).move_to(formula)

        self.play(FadeIn(formula_bg), Write(formula))
        self.wait(2)