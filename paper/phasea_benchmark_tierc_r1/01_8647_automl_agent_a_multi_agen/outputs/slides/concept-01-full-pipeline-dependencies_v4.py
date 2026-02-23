from manim import *

class Concept01FullPipelineDependencies(Scene):
    def construct(self):
        # 1. Technical background using NumberPlane
        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 2,
                "stroke_opacity": 0.2
            }
        )
        self.add(number_plane)

        # 2. Define the Pipeline stages
        stage_names = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        circles = VGroup()
        labels = VGroup()

        for name in stage_names:
            c = Circle(radius=0.9, color=BLUE, fill_opacity=0.2)
            lbl = Text(name.replace(" ", "\n"), font_size=22)
            circles.add(c)
            labels.add(lbl)

        circles.arrange(RIGHT, buff=1.0).shift(UP * 0.5)
        for i in range(len(circles)):
            labels[i].move_to(circles[i].get_center())

        # 3. Create thick Arrows connecting the circles
        arrows = VGroup()
        for i in range(len(circles) - 1):
            arr = Arrow(
                circles[i].get_right(),
                circles[i+1].get_left(),
                buff=0.1,
                stroke_width=10,
                color=WHITE
            )
            arrows.add(arr)

        # 4. Pipeline Formula
        formula = MathTex(
            r"Pipeline = \{Data \to Preprocessing \to Model \to HPO \to Deployment\}",
            font_size=32
        ).to_edge(DOWN, buff=0.8)

        # Add initial objects
        self.add(circles, labels, arrows, formula)
        self.wait(1)

        # 5. Pulse Animation for 'Data Retrieval'
        # Using two sequential animations to simulate a pulse without using potentially undefined rate functions
        self.play(circles[0].animate.scale(1.2), run_time=0.4)
        self.play(circles[0].animate.scale(1/1.2), run_time=0.4)

        # 6. Propagation Ripple (Color Change from Blue to Gold)
        # We animate the color change through the sequence of circles and arrows
        self.play(circles[0].animate.set_color(GOLD), run_time=0.3)
        
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                circles[i+1].animate.set_color(GOLD),
                run_time=0.6
            )

        self.wait(2)

        # Final cleanup
        self.play(
            FadeOut(circles),
            FadeOut(labels),
            FadeOut(arrows),
            FadeOut(formula)
        )
        self.wait(1)