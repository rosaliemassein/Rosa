from manim import *

class ConceptPipelineDependencies(Scene):
    def construct(self):
        # 1. Background: Technical feel with NumberPlane
        # Using basic BLUE to avoid undefined shade errors
        plane = NumberPlane(
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
                "stroke_opacity": 0.2
            }
        )
        self.add(plane)

        # 2. Formula at the top
        formula = MathTex(
            r"\text{Pipeline} = \{ \text{Data} \to \text{Preprocessing} \to \text{Model} \to \text{HPO} \to \text{Deployment} \}",
            font_size=30
        )
        formula.to_edge(UP, buff=0.5)
        self.play(Write(formula))

        # 3. Create the circles (Nodes)
        # Using BLUE as the base color
        c1 = Circle(radius=0.8, color=BLUE, fill_opacity=0.2).shift(LEFT * 4.5)
        c2 = Circle(radius=0.8, color=BLUE, fill_opacity=0.2).shift(LEFT * 1.5)
        c3 = Circle(radius=0.8, color=BLUE, fill_opacity=0.2).shift(RIGHT * 1.5)
        c4 = Circle(radius=0.8, color=BLUE, fill_opacity=0.2).shift(RIGHT * 4.5)

        # Labels for the circles
        l1 = Text("Data\nRetrieval", font_size=16).move_to(c1.get_center())
        l2 = Text("Preprocessing", font_size=16).move_to(c2.get_center())
        l3 = Text("Model\nSearch", font_size=16).move_to(c3.get_center())
        l4 = Text("Deployment", font_size=16).move_to(c4.get_center())

        # 4. Thick Arrows connecting circles
        # Using BLUE for initial arrows
        arrow_kwargs = {"stroke_width": 8, "color": BLUE, "buff": 0.1}
        a1 = Arrow(c1.get_right(), c2.get_left(), **arrow_kwargs)
        a2 = Arrow(c2.get_right(), c3.get_left(), **arrow_kwargs)
        a3 = Arrow(c3.get_right(), c4.get_left(), **arrow_kwargs)

        pipeline_group = VGroup(c1, c2, c3, c4, l1, l2, l3, l4, a1, a2, a3)
        pipeline_group.shift(DOWN * 0.5)

        # Initial display
        self.play(
            Create(VGroup(c1, c2, c3, c4)),
            Write(VGroup(l1, l2, l3, l4)),
            run_time=1.5
        )
        self.play(Create(VGroup(a1, a2, a3)))
        self.wait(1)

        # 5. Ripple Animation: Pulse 'Data Retrieval' and propagate color change to GOLD
        # Pulse animation (using Indicate)
        self.play(Indicate(c1, scale_factor=1.2, color=GOLD), run_time=1)

        # Color Propagation sequence through the pipeline
        propagation_time = 0.5
        self.play(c1.animate.set_color(GOLD).set_fill(GOLD, opacity=0.4), run_time=propagation_time)
        self.play(a1.animate.set_color(GOLD), run_time=propagation_time)
        self.play(c2.animate.set_color(GOLD).set_fill(GOLD, opacity=0.4), run_time=propagation_time)
        self.play(a2.animate.set_color(GOLD), run_time=propagation_time)
        self.play(c3.animate.set_color(GOLD).set_fill(GOLD, opacity=0.4), run_time=propagation_time)
        self.play(a3.animate.set_color(GOLD), run_time=propagation_time)
        self.play(c4.animate.set_color(GOLD).set_fill(GOLD, opacity=0.4), run_time=propagation_time)

        self.wait(2)

        # Clean up
        self.play(
            FadeOut(pipeline_group),
            FadeOut(formula),
            FadeOut(plane)
        )
        self.wait(1)