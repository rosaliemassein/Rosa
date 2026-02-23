from manim import *

class Concept03PseudoExecutionHandoff(Scene):
    def construct(self):
        # Top half: Data Agent
        data_agent = Text("Data Agent").to_edge(UP)
        data_block = Rectangle(width=3, height=1).next_to(data_agent, DOWN)

        # Bottom half: Model Agent
        model_agent = Text("Model Agent").to_edge(DOWN)
        model_task_block = Rectangle(width=3, height=1).next_to(model_agent, UP)

        # Arrow and insights
        arrow = Arrow(data_block.get_bottom(), model_task_block.get_top())
        data_insights = Text("O_d").move_to(arrow.get_center())

        # ValueTracker for Search Efficiency
        search_efficiency = Text("Search Efficiency: 0%").to_edge(RIGHT)

        # Animations
        self.play(Create(data_agent), Create(data_block))
        self.wait(0.5)
        self.play(Create(model_agent), Create(model_task_block))
        self.wait(0.5)
        self.play(FadeIn(data_insights), Create(arrow))
        self.wait(0.5)
        self.play(Transform(search_efficiency, Text("Search Efficiency: 30%").to_edge(RIGHT)), run_time=1)
        self.wait(0.5)
        self.play(Transform(search_efficiency, Text("Search Efficiency: 60%").to_edge(RIGHT)), run_time=1)
        self.wait(0.5)
        self.play(Transform(search_efficiency, Text("Search Efficiency: 90%").to_edge(RIGHT)), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(data_insights), FadeOut(arrow))

        # Equation
        equation = MathTex(r"s_i^m = \mathrm{PD}(R, \mathcal{A}_m, \mathbf{p}_i, O_i^d)").to_edge(DOWN)
        self.play(FadeIn(equation))
        self.wait(2)