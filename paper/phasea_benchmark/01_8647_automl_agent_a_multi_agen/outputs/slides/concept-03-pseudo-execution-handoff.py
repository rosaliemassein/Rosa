from manim import *

class PseudoExecutionHandoff(Scene):
    def construct(self):
        data_agent = Text("Data Agent (A_d)").shift(UP * 3)
        model_agent = Text("Model Agent (A_m)").shift(DOWN * 3)

        data_block = Rectangle(height=1, width=2).next_to(data_agent, DOWN)
        model_task_block = Rectangle(height=1, width=3).next_to(model_agent, DOWN)
        
        data_insights = Text("O_d (Data Insights)").next_to(data_block, RIGHT)
        
        arrow = Arrow(data_block.get_bottom(), model_task_block.get_top()).set_color(BLUE)

        search_efficiency = Rectangle(height=0.5, width=4).to_edge(RIGHT)
        efficiency_label = Text("Search Efficiency").next_to(search_efficiency, UP)

        self.play(Create(data_agent), Create(model_agent))
        self.wait(1)
        
        self.play(Create(data_block), Create(data_insights))
        self.wait(1)
        
        self.play(FadeIn(arrow), Create(model_task_block))
        self.wait(1)
        
        self.play(Transform(search_efficiency, search_efficiency.scale(2).shift(DOWN * 1.5)), Create(efficiency_label))
        self.wait(1)