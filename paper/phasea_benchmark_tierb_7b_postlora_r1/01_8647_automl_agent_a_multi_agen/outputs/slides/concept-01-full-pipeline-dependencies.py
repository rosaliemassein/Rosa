from manim import *

class Concept01FullPipelineDependencies(Scene):
    def construct(self):
        # Create the circle nodes
        data_retrieval = Circle(radius=1.5, color=BLUE)
        preprocessing = Circle(radius=1.5, color=GREEN)
        model_search = Circle(radius=1.5, color=RED)
        deployment = Circle(radius=1.5, color=YELLOW)

        # Position the circles
        data_retrieval.to_edge(UP)
        preprocessing.next_to(data_retrieval, DOWN).shift(DOWN*0.5)
        model_search.next_to(preprocessing, RIGHT).shift(RIGHT*1.5)
        deployment.next_to(model_search, DOWN).shift(DOWN*0.5)

        # Create the arrows
        arrow1 = Arrow(data_retrieval.get_bottom(), preprocessing.get_top())
        arrow2 = Arrow(preprocessing.get_bottom(), model_search.get_top())
        arrow3 = Arrow(model_search.get_bottom(), deployment.get_top())

        # Add the nodes and arrows to the scene
        self.add(data_retrieval, preprocessing, model_search, deployment)
        self.add(arrow1, arrow2, arrow3)

        # Pulse animation for Data Retrieval circle
        pulse = Indicate(data_retrieval, color=RED)
        self.play(pulse)

        # Propagate color change through arrows and Deployment circle
        arrow1.set_color(GOLD)
        arrow2.set_color(GOLD)
        arrow3.set_color(GOLD)
        deployment.set_color(GOLD)

        self.wait(2)