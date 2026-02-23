from manim import *

class ConceptPipelineDependencies(Scene):
    def construct(self):
        # 1. Data and Text Definitions
        voice_text = (
            "In traditional AutoML, we often treat model selection and data processing as isolated steps. "
            "But in a full-pipeline system, they are deeply interconnected. Imagine your raw data as the foundation; "
            "a change here, like a specific preprocessing technique, ripples through the entire structure, "
            "dictating which models are viable and which hyperparameters need tuning. AutoML-Agent manages "
            "this complexity by mapping the entire flow from initial data retrieval all the way to a deployment-ready inference endpoint."
        )
        formula_str = r"\text{Pipeline} = \{ \text{Data} \to \text{Preprocessing} \to \text{Model} \to \text{HPO} \to \text{Deployment} \}"

        # 2. Background
        grid = NumberPlane(background_line_style={"stroke_opacity": 0.2})
        self.add(grid)

        # 3. Titles and Narrations
        title = Text("Full-Pipeline AutoML Dependencies").scale(0.7).to_edge(UP)
        formula_tex = MathTex(formula_str).scale(0.6).next_to(title, DOWN, buff=0.3)
        # Using string "ITALIC" instead of constant to avoid undefined identifier errors
        narration_text = Text(voice_text, slant="ITALIC", line_spacing=1.5).scale(0.25).to_edge(DOWN, buff=0.4)

        # 4. Pipeline Elements (Circles and Labels)
        labels = ["Data Retrieval", "Preprocessing", "Model Search", "Deployment"]
        # Use starting colors that will eventually change to GOLD
        colors = [BLUE, GREEN, RED, WHITE]
        
        circles = VGroup(*[
            VGroup(
                Circle(radius=0.7, color=colors[i], fill_opacity=0.3),
                Text(labels[i]).scale(0.35)
            ) for i in range(len(labels))
        ]).arrange(RIGHT, buff=1.2).shift(UP * 0.5)

        # Thick Arrows connecting the circles
        arrows = VGroup(*[
            Arrow(
                circles[i].get_right(), 
                circles[i+1].get_left(), 
                stroke_width=10, 
                buff=0.1,
                max_tip_length_to_length_ratio=0.2
            )
            for i in range(len(circles) - 1)
        ])

        # 5. Initialization
        self.add(title, formula_tex)
        self.play(
            Create(circles),
            Create(arrows),
            run_time=2
        )
        self.wait(0.5)

        # 6. Ripple Animation
        # Pulse the first circle (Data Retrieval)
        self.play(
            circles[0][0].animate.scale(1.3).set_color(GOLD).set_fill(opacity=0.6),
            circles[0][1].animate.set_color(GOLD),
            run_time=0.8
        )
        self.play(circles[0][0].animate.scale(1/1.3), run_time=0.3)

        # Propagate the change through arrows and subsequent circles
        for i in range(len(arrows)):
            self.play(
                arrows[i].animate.set_color(GOLD).set_stroke(width=15),
                circles[i+1][0].animate.set_color(GOLD).set_fill(opacity=0.6),
                circles[i+1][1].animate.set_color(GOLD),
                run_time=0.7
            )

        # 7. Final narration and image placeholder
        # Creating a placeholder for img-1.jpeg
        image_placeholder = Rectangle(height=1.5, width=2.5, color=GREY, fill_opacity=0.2).next_to(formula_tex, DOWN, buff=0.2)
        image_text = Text("img-1.jpeg reference", font_size=14).move_to(image_placeholder)
        
        self.play(
            FadeIn(image_placeholder),
            FadeIn(image_text),
            Write(narration_text),
            run_time=3
        )
        
        self.wait(3)