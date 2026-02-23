from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Background Technical Feel
        plane = NumberPlane(background_line_style={"stroke_opacity": 0.2})
        self.add(plane)

        # 2. Define Circles and Labels
        titles = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        circles = VGroup()
        labels = VGroup()

        for title in titles:
            circle = Circle(radius=0.9, color=BLUE, fill_opacity=0.2)
            label = Text(title, font_size=22)
            label.move_to(circle.get_center())
            circles.add(circle)
            labels.add(label)

        # Group and position them
        nodes = VGroup(*[VGroup(circles[i], labels[i]) for i in range(len(titles))])
        nodes.arrange(RIGHT, buff=1.2).shift(UP * 0.5)

        # 3. Define thick arrows between circles
        arrows = VGroup()
        for i in range(len(titles) - 1):
            arrow = Arrow(
                circles[i].get_right(),
                circles[i+1].get_left(),
                buff=0.1,
                stroke_width=10,
                color=BLUE,
                max_tip_length_to_stroke_width_ratio=2
            )
            arrows.add(arrow)

        # 4. Define the formula at the bottom
        formula = MathTex(
            r"\text{Pipeline} = \{ \text{Data} \to \text{Preprocessing} \to \text{Model} \to \text{HPO} \to \text{Deployment} \}",
            font_size=36
        ).to_edge(DOWN, buff=0.8)

        # --- ANIMATION SEQUENCE ---

        # Show initial pipeline
        self.play(
            LaggedStart(
                Create(nodes),
                Create(arrows),
                Write(formula),
                lag_ratio=0.3
            ),
            run_time=3
        )
        self.wait(1)

        # Ripple Animation: Pulse the first circle
        self.play(
            Indicate(circles[0], color=GOLD, scale_factor=1.2),
            labels[0].animate.set_color(GOLD),
            run_time=1.5
        )

        # Propagate color change from Blue to Gold through the flow
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                circles[i+1].animate.set_color(GOLD),
                labels[i+1].animate.set_color(GOLD),
                run_time=0.8
            )

        self.wait(3)