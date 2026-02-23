from manim import *

class ZeroShotClassification(Scene):
    def construct(self):
        # 1. Setup Vector v and Matrix X
        # Vector v representation
        v_label = MathTex(r"\mathbf{v}", color=RED).to_edge(LEFT, buff=1.0)
        v_box = Rectangle(height=3, width=0.6, color=RED).next_to(v_label, RIGHT)
        v_elements = VGroup(*[Line(LEFT*0.2, RIGHT*0.2) for _ in range(5)]).arrange(DOWN, buff=0.4).move_to(v_box)
        vector_v = VGroup(v_label, v_box, v_elements)

        # Matrix X (Countries)
        countries = ["USA", "France", "Canada", "Japan", "Brazil", "India", "China", "Germany"]
        x_label = MathTex(r"\mathbf{X}", color=BLUE).shift(RIGHT * 0.5 + UP * 2.5)
        
        # Create matrix rows manually
        matrix_rows = VGroup()
        for name in countries:
            row_rect = Rectangle(height=0.4, width=2.5, color=BLUE, fill_opacity=0.2)
            row_text = Text(name, font_size=20)
            matrix_rows.add(VGroup(row_rect, row_text))
        
        matrix_rows.arrange(DOWN, buff=0.1).next_to(x_label, DOWN)
        
        # 2. Narration & Initial Display
        voice_1 = Text("Once the model is trained, we can use it as a zero-shot classifier.", font_size=22).to_edge(UP)
        self.play(Write(voice_1))
        self.play(FadeIn(vector_v), FadeIn(x_label), FadeIn(matrix_rows))
        self.wait(1)

        # 3. Vector Representation v
        voice_2 = Text("For a new image, we generate its vector representation, v.", font_size=22).to_edge(UP)
        self.play(Transform(voice_1, voice_2))
        self.play(vector_v.animate.scale(1.1).set_color(YELLOW), run_time=0.5)
        self.play(vector_v.animate.scale(1/1.1).set_color(RED), run_time=0.5)
        self.wait(1)

        # 4. Dot Product Operation
        voice_3 = Text("Compare v against matrix X containing text embeddings.", font_size=22).to_edge(UP)
        self.play(Transform(voice_1, voice_3))
        
        dot_results = VGroup()
        for i in range(len(matrix_rows)):
            # Manual highlight instead of SurroundRectangle
            highlight = Rectangle(
                width=matrix_rows[i].width + 0.2, 
                height=matrix_rows[i].height + 0.1, 
                color=YELLOW
            ).move_to(matrix_rows[i])
            
            dot_tex = MathTex(r"\mathbf{X}_{" + str(i+1) + r"}^T \mathbf{v}", font_size=20).next_to(matrix_rows[i], RIGHT, buff=0.5)
            
            if i < 3: # Animate a few for the effect
                self.play(Create(highlight), run_time=0.2)
                self.play(Write(dot_tex), run_time=0.2)
                self.play(FadeOut(highlight), run_time=0.1)
            else:
                self.add(dot_tex)
            dot_results.add(dot_tex)
        
        self.wait(1)

        # 5. Softmax and Bar Chart
        voice_4 = Text("Applying softmax, we get a probability distribution.", font_size=22).to_edge(UP)
        self.play(Transform(voice_1, voice_4))
        
        # Manual Bar Chart Construction for compatibility
        chart_origin = RIGHT * 4 + DOWN * 1.5
        x_axis = Line(chart_origin, chart_origin + RIGHT * 5)
        y_axis = Line(chart_origin, chart_origin + UP * 3)
        
        bars = VGroup()
        for i in range(len(countries)):
            bar = Rectangle(
                height=0.1, # Initial height
                width=0.4, 
                fill_opacity=0.8, 
                color=BLUE, 
                stroke_width=1
            ).move_to(chart_origin + RIGHT * (0.6 * i + 0.4), aligned_edge=DOWN)
            bars.add(bar)

        self.play(
            FadeOut(matrix_rows),
            FadeOut(dot_results),
            FadeOut(x_label),
            Create(x_axis),
            Create(y_axis),
            Create(bars)
        )
        
        # Probabilities: France (index 1) is high
        new_heights = [0.2, 2.5, 0.3, 0.1, 0.2, 0.1, 0.1, 0.1]
        growth_anims = []
        for bar, h in zip(bars, new_heights):
            growth_anims.append(bar.animate.stretch_to_fit_height(h, about_edge=DOWN))
            
        self.play(*growth_anims, run_time=2)
        
        voice_5 = Text("The country with the highest score is the prediction.", font_size=22).to_edge(UP)
        self.play(Transform(voice_1, voice_5))
        self.play(bars[1].animate.set_color(GREEN)) # France bar
        
        france_label = Text("France", font_size=18).next_to(bars[1], UP)
        self.play(Write(france_label))
        self.wait(1)

        # 6. Formula
        formula = MathTex(
            r"h(\mathbf{v};\mathbf{X})=\frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}",
            font_size=32
        ).to_edge(RIGHT, buff=1).shift(UP * 2)
        
        self.play(Write(formula))
        self.wait(1)

        # 7. Final Ask & Image
        voice_6 = Text("Which of these country descriptions does it look like most?", font_size=22).to_edge(UP)
        self.play(Transform(voice_1, voice_6))
        
        # Simple placeholder for the image
        img_placeholder = Rectangle(height=2, width=2.5, color=WHITE).to_edge(LEFT, buff=0.8).shift(UP*0.5)
        img_text = Text("Image Reference", font_size=16).move_to(img_placeholder)
        
        try:
            actual_img = ImageMobject("img-8.jpeg").scale_to_fit_height(2).move_to(img_placeholder)
            self.play(FadeIn(actual_img))
        except:
            self.play(Create(img_placeholder), Write(img_text))
            
        self.play(FadeOut(vector_v))
        self.wait(2)

        # Final Cleanup
        self.play(FadeOut(Group(*self.mobjects)))
        final_msg = Text("Zero-Shot Classification Mechanism", font_size=32)
        self.play(Write(final_msg))
        self.wait(2)