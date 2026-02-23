from manim import *

class ConceptPipelineDependencies(Scene):
    def construct(self):
        # Define the circles for each step of the pipeline
        data_circle = Circle(color=BLUE)
        preprocess_circle = Circle(color=GREEN)
        model_circle = Circle(color=YELLOW)
        deployment_circle = Circle(color=RED)

        # Arrange the circles
        arranged_circles = arrange([data_circle, preprocess_circle, model_circle, deployment_circle], buff=1.5)

        # Draw arrows between the circles
        data_to_preprocess = Arrow(start=arranged_circles[0].get_center(), end=arranged_circles[1].get_center())
        preprocess_to_model = Arrow(start=arranged_circles[1].get_center(), end=arranged_circles[2].get_center())
        model_to_hpo = Arrow(start=arranged_circles[2].get_center(), end=arranged_circles[3].get_center())
        hpo_to_deployment = Arrow(start=arranged_circles[3].get_center(), end=arranged_circles[4].get_center())

        # Show the circles and arrows
        self.play(Create(data_circle), Create(preprocess_circle), 
                Create(model_circle), Create(deployment_circle),
                Create(data_to_preprocess), Create(preprocess_to_model),
                Create(model_to_hpo), Create(hpo_to_deployment))

        # Narration
        self.wait(2)
        self.play(
            Transform(data_circle, Circle(color=BLUE, color_opacity=0.5)),
            Transform(preprocess_circle, Circle(color=GREEN, color_opacity=0.7)),
            Transform(model_circle, Circle(color=YELLOW, color_opacity=1.0)),
            Transform(deployment_circle, Circle(color=RED, color_opacity=0.5))
        )
        self.wait(2)

        # Formula
        formula = MathTex(r"\{Data \\rightarrow Preprocessing \\rightarrow Model \\rightarrow HPO \\rightarrow Deployment\}")
        self.play(FadeIn(formula, shift=UP))

        # Wait for the narration and formula
        self.wait(5)