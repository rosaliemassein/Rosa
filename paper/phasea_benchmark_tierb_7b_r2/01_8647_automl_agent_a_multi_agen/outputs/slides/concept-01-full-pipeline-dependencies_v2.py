from manim import *

class ConceptPipeline(Scene):
    def construct(self):
        # Technical background using simple lines instead of NumberPlane
        grid = VGroup(*[
            Line(7 * LEFT + y * UP, 7 * RIGHT + y * UP, stroke_width=1, stroke_opacity=0.2)
            for y in range(-4, 5)
        ])
        grid.add(*[
            Line(4 * DOWN + x * RIGHT, 4 * UP + x * RIGHT, stroke_width=1, stroke_opacity=0.2)
            for x in range(-7, 8)
        ])
        self.add(grid)

        # Formula reference at the top
        formula = MathTex(
            r"\text{Pipeline} = \{ \text{Data} \to \text{Preprocessing} \to \text{Model} \to \text{HPO} \to \text{Deployment} \}",
            font_size=30
        ).to_edge(UP)
        self.add(formula)

        # Pipeline steps components
        steps_text = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        circles = VGroup()
        labels = VGroup()
        
        for i, text in enumerate(steps_text):
            circle = Circle(radius=0.75, color=BLUE, fill_opacity=0.1)
            label = Text(text.replace(" ", "\n"), font_size=20)
            
            # Arrange circles vertically
            circle.move_to(UP * 2.2 + i * DOWN * 1.6)
            label.move_to(circle.get_center())
            
            circles.add(circle)
            labels.add(label)

        # Create thick arrows connecting the steps
        arrows = VGroup()
        for i in range(len(circles) - 1):
            arrow = Arrow(
                circles[i].get_bottom(), 
                circles[i+1].get_top(), 
                buff=0.1, 
                stroke_width=6, 
                color=BLUE,
                max_tip_length_to_length_ratio=0.15
            )
            arrows.add(arrow)

        # Initial display
        self.play(
            Create(circles),
            Write(labels),
            Create(arrows),
            run_time=2
        )
        self.wait(1)

        # "Ripples through" animation
        # 1. Pulse Data Retrieval
        self.play(Indicate(circles[0], color=BLUE, scale_factor=1.3), run_time=1)

        # 2. Propagate color change (Blue to Gold) through arrows and circles
        propagation_time = 0.5
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                circles[i+1].animate.set_color(GOLD),
                run_time=propagation_time
            )
            
        self.wait(2)

        # Final highlight of the deployment circle
        self.play(
            circles[-1].animate.scale(1.2),
            Flash(circles[-1], color=GOLD, line_length=0.3),
            run_time=1
        )
        self.play(circles[-1].animate.scale(1/1.2))
        
        self.wait(2)