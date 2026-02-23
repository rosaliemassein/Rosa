from manim import *

class ConceptFullPipelineDependencies(Scene):
    def construct(self):
        # 1. Background Setup
        number_plane = NumberPlane(
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "stroke_opacity": 0.2
            }
        )
        self.add(number_plane)

        # 2. Creating Pipeline Components
        labels = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        # Start with consistent blue theme
        
        nodes = VGroup()
        for label_text in labels:
            circle = Circle(radius=1.1, color=BLUE, fill_opacity=0.2, fill_color=BLUE)
            text = Text(label_text.replace(" ", "\n"), font_size=24, color=WHITE)
            node = VGroup(circle, text)
            nodes.add(node)
        
        nodes.arrange(RIGHT, buff=0.8).move_to(ORIGIN)

        # Create thick arrows connecting them
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                nodes[i].get_right(), 
                nodes[i+1].get_left(), 
                buff=0.1, 
                stroke_width=10, 
                color=WHITE
            )
            arrows.add(arrow)

        # Formula at the top
        # Using MathTex for the specific formula provided
        formula = MathTex(
            r"\text{Pipeline} = \{ \text{Data} \to \text{Preprocessing} \to \text{Model} \to \text{HPO} \to \text{Deployment} \}",
            font_size=34
        ).to_edge(UP, buff=0.5)

        # 3. Initial Animation: Build the structure
        self.play(Write(formula))
        self.play(
            LaggedStart(
                *[Create(node) for node in nodes],
                *[Create(arrow) for arrow in arrows],
                lag_ratio=0.2
            )
        )
        self.wait(1)

        # 4. The "Ripple" Animation
        # Pulse animation on 'Data Retrieval'
        self.play(Indicate(nodes[0], color=GOLD, scale_factor=1.2), run_time=1)
        
        # Propagate color change (Blue -> Gold) through arrows and circles
        propagation_anims = []
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD),
                nodes[i+1][0].animate.set_color(GOLD).set_fill(GOLD, opacity=0.3),
                run_time=0.6
            )

        self.wait(2)

        # 5. Handle Image Reference 
        # Wrapping in a try/except or conditional to handle missing local files gracefully
        try:
            image_ref = ImageMobject("img-1.jpeg")
            image_ref.scale(0.5).to_edge(DOWN, buff=0.2)
            self.play(FadeIn(image_ref))
        except:
            image_label = Text("Image: img-1.jpeg", font_size=16, color=GRAY).to_edge(DOWN)
            self.add(image_label)

        self.wait(2)
        
        # 6. Final Fade Out
        self.play(
            FadeOut(nodes),
            FadeOut(arrows),
            FadeOut(formula),
            FadeOut(number_plane)
        )
        self.wait(1)