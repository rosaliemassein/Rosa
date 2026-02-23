from manim import *

class FullPipelineDependencies(Scene):
    def construct(self):
        # Create a manual grid for a technical feel to replace NumberPlane
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line([x, -4, 0], [x, 4, 0], stroke_opacity=0.1, stroke_width=1))
        for y in range(-4, 5):
            grid.add(Line([-7, y, 0], [7, y, 0], stroke_opacity=0.1, stroke_width=1))
        self.add(grid)

        # Pipeline Formula reference
        formula = MathTex(
            r"\text{Pipeline} = \{ \text{Data} \to \text{Preprocessing} \to \text{Model} \to \text{HPO} \to \text{Deployment} \}", 
            font_size=24
        )
        formula.to_edge(UP, buff=0.5)
        self.add(formula)

        # Define steps for the four large circles
        steps_text = ["Data\nRetrieval", "Pre-\nprocessing", "Model\nSearch", "Deploy-\nment"]
        circles = VGroup()
        labels = VGroup()
        
        for i, text in enumerate(steps_text):
            # Create circles with technical styling
            c = Circle(radius=1.1, color=BLUE, fill_opacity=0.2)
            t = Text(text, font_size=20)
            # Distribute circles horizontally
            c.move_to(RIGHT * (i * 3.6 - 5.4))
            t.move_to(c.get_center())
            circles.add(c)
            labels.add(t)

        # Create thick arrows connecting the steps
        arrows = VGroup()
        for i in range(len(circles) - 1):
            arr = Arrow(
                circles[i].get_right(), 
                circles[i+1].get_left(), 
                stroke_width=10, 
                color=BLUE, 
                buff=0.1
            )
            arrows.add(arr)

        # Add initial pipeline to the scene
        self.add(circles, labels, arrows)

        # 1. Apply pulse animation to the 'Data Retrieval' circle
        self.play(Indicate(circles[0], color=GOLD, scale_factor=1.2), run_time=1.5)
        self.wait(0.1)

        # 2. Propagate a color change from blue to gold through arrows to 'Deployment'
        # We loop through the pipeline to simulate the "ripple" effect
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                circles[i+1].animate.set_color(GOLD),
                labels[i+1].animate.set_color(GOLD),
                run_time=0.8
            )

        # Final emphasis on the end-to-end nature
        self.play(
            circles.animate.set_stroke(width=8),
            formula.animate.set_color(GOLD),
            run_time=1
        )

        self.wait(2)