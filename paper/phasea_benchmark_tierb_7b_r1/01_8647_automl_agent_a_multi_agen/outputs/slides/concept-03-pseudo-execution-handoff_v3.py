from manim import *

class Concept03PseudoExecutionHandoff(Scene):
    def construct(self):
        data_agent = Text("Data Agent (A_d)").to_edge(UP)
        model_agent = Text("Model Agent (A_m)").to_edge(DOWN)

        data_block = Rectangle(height=1, width=2.5).next_to(data_agent, DOWN).shift(DOWN * 0.5)
        data_insights = Text("O_d (Data Insights)").next_to(data_block, DOWN)

        arrow = Arrow(start=data_block.get_bottom(), end=model_agent.get_top()).shift(LEFT * 0.5)

        model_task = Text("s_m (Model Task)").next_to(model_agent, UP).shift(UP * 0.5)

        search_efficiency = Rectangle(height=0.3, width=4).next_to(model_agent, RIGHT)

        self.play(Create(data_agent), Create(model_agent))
        self.wait(1)
        self.play(Create(data_block), Write(data_insights))
        self.wait(1)
        self.play(Create(arrow))
        self.wait(1)
        self.play(Create(model_task), Transform(search_efficiency, search_efficiency.scale(0.5).shift(RIGHT * 2)))
        self.wait(1)