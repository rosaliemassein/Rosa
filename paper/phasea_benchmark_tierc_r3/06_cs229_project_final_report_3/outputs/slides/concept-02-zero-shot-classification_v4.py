from manim import *

class ZeroShotClassification(Scene):
    def construct(self):
        # 1. Formula reference
        formula = MathTex(
            r"h(\mathbf{v};\mathbf{X}) = \frac{\exp(\mathbf{X}\mathbf{v})}{\sum_{j=1}^{N}\exp(\mathbf{X}_{j}^{T}\mathbf{v})}",
            font_size=36
        ).to_edge(UP, buff=0.5)

        # 2. Image representation (with fallback placeholder)
        try:
            image = ImageMobject("img-8.jpeg").set_height(2.2)
        except:
            image = Rectangle(width=3, height=2, color=BLUE)
            image.add(Text("Image", font_size=16))
        
        image.to_edge(LEFT, buff=0.7).shift(UP * 0.2)

        # 3. Vector v (using Arrow instead of Vector to avoid potential missing identifier)
        v_arrow = Arrow(start=LEFT, end=RIGHT, color=GREEN, buff=0).scale(0.7)
        v_arrow.next_to(image, RIGHT, buff=0.4)
        v_label = MathTex(r"\mathbf{v}", color=GREEN).next_to(v_arrow, UP, buff=0.1)

        # 4. Matrix X (using individual Text objects for easy row-by-row highlighting)
        # This replaces the Matrix class to ensure maximum compatibility
        countries = ["USA", "Canada", "Mexico", "Brazil", "France", "Japan", "India"]
        country_rows = VGroup(*[Text(c, font_size=20) for c in countries]).arrange(DOWN, buff=0.3)
        
        # Create brackets for the matrix look
        lb = MathTex(r"\left[", font_size=100).next_to(country_rows, LEFT, buff=0.1)
        rb = MathTex(r"\right]", font_size=100).next_to(country_rows, RIGHT, buff=0.1)
        
        matrix_group = VGroup(country_rows, lb, rb).next_to(v_arrow, RIGHT, buff=0.5)
        matrix_label = MathTex(r"\mathbf{X}").next_to(matrix_group, UP, buff=0.2)

        # 5. Bar Chart (Manually drawn using Rectangles to avoid BarChart class issues)
        chart_base = Line(LEFT, RIGHT).scale(1.5).shift(RIGHT * 4.8 + DOWN * 2.0)
        bars = VGroup()
        for i in range(len(countries)):
            # Start bars at a baseline height
            bar = Rectangle(width=0.3, height=0.1, fill_opacity=0.8, color=BLUE, stroke_width=1)
            bar.move_to(chart_base.get_left() + RIGHT * (i * 0.45 + 0.3), aligned_edge=DOWN)
            bars.add(bar)

        # --- Execution Sequence ---
        self.add(formula)
        self.play(FadeIn(image))
        self.play(GrowArrow(v_arrow), Write(v_label))
        self.play(Write(matrix_group), Write(matrix_label))
        self.play(Create(chart_base), FadeIn(bars))
        self.wait(0.5)

        # 6. Pulse highlight and update chart in real-time
        for i in range(len(countries)):
            # Create a highlight for the current row being compared
            highlight = SurroundingRectangle(country_rows[i], color=RED, buff=0.1)
            self.play(Create(highlight), run_time=0.15)
            
            # Update bar height to simulate Softmax results
            # France (index 4) is the target winner
            if i == 4:
                self.play(
                    bars[i].animate.stretch_to_fit_height(2.8, about_edge=DOWN).set_color(YELLOW),
                    run_time=0.4
                )
            else:
                self.play(
                    bars[i].animate.stretch_to_fit_height(0.15 + (i % 3) * 0.2, about_edge=DOWN),
                    run_time=0.1
                )
            self.play(FadeOut(highlight), run_time=0.1)

        # Final result highlight
        self.play(Indicate(bars[4], scale_factor=1.3))
        self.wait(2)