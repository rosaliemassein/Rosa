from manim import *

class FullPipelineDependencies(Scene):
    def construct(self):
        # Background: Manual Grid instead of NumberPlane to avoid restricted features
        grid = VGroup()
        for x in range(-7, 8):
            grid.add(Line([x, -4, 0], [x, 4, 0], stroke_width=0.5, color=GRAY, stroke_opacity=0.3))
        for y in range(-4, 5):
            grid.add(Line([-7, y, 0], [7, y, 0], stroke_width=0.5, color=GRAY, stroke_opacity=0.3))
        self.add(grid)

        # Pipeline steps configuration
        step_names = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        colors = [BLUE, BLUE, BLUE, BLUE]
        positions = [LEFT * 4.5, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4.5]
        
        circles = VGroup()
        labels = VGroup()
        
        for name, color, pos in zip(step_names, colors, positions):
            circle = Circle(radius=0.9, color=color, fill_opacity=0.2)
            circle.move_to(pos)
            label = Text(name, font_size=20).next_to(circle, DOWN)
            circles.add(circle)
            labels.add(label)

        # Thick arrows connecting the circles
        arrows = VGroup()
        for i in range(len(circles) - 1):
            arrow = Arrow(
                circles[i].get_right(), 
                circles[i+1].get_left(), 
                buff=0.1, 
                stroke_width=8,
                color=BLUE
            )
            arrows.add(arrow)

        # Formula at the top
        formula = MathTex(
            r"Pipeline = \{Data \to Preprocessing \to Model \to HPO \to Deployment\}",
            font_size=30
        ).to_edge(UP)

        # Initial render
        self.add(circles, labels, arrows, formula)

        # Animation sequence
        # 1. Pulse 'Data Retrieval'
        self.play(Indicate(circles[0], color=WHITE, scale_factor=1.2), run_time=1.5)

        # 2. Ripple color change from Blue to Gold through the pipeline
        ripple_animations = []
        for i in range(len(circles)):
            # Change circle color
            ripple_animations.append(circles[i].animate.set_color(GOLD).set_fill(GOLD, opacity=0.4))
            # Change arrow color (if exists)
            if i < len(arrows):
                ripple_animations.append(arrows[i].animate.set_color(GOLD))

        self.play(
            LaggedStart(*ripple_animations, lag_ratio=0.4),
            run_time=4
        )

        self.wait(2)