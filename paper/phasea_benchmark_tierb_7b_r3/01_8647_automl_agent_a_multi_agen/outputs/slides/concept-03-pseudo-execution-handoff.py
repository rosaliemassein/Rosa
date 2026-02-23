from manim import *
import math

class PseudoExecutionHandoff(Scene):
    def construct(self):
        # Create agents
        data_agent = Text("Data Agent (A_d)").scale(0.8).to_edge(UP)
        model_agent = Text("Model Agent (A_m)").scale(0.8).to_edge(DOWN)

        # Create task blocks
        task_block_data = Text("Data Insights (O_d)").scale(0.8).next_to(data_agent, DOWN)
        task_block_model = Text("Sub-tasks (s_m)").scale(0.8).next_to(model_agent, DOWN)

        # Create arrow to show information handoff
        arrow = Arrow(data_agent.get_bottom(), model_agent.get_top(), color=BLUE)

        # Create ValueTracker for search efficiency
        efficiency_bar = Rectangle(width=2, height=0.5, color=GREEN).next_to(model_agent, RIGHT).shift(LEFT * 2)
        efficiency_text = Text("Search Efficiency").scale(0.8).next_to(efficiency_bar, UP)

        # Animate
        self.play(Create(data_agent))
        self.wait(0.5)
        self.play(Create(task_block_data))
        self.wait(0.5)
        self.play(Create(model_agent))
        self.wait(0.5)
        self.play(FadeIn(arrow), Write(efficiency_text))
        self.wait(0.5)
        self.play(Create(task_block_model), Transform(efficiency_bar, Rectangle(width=3, height=0.5, color=GREEN)))
        self.wait(1)
        self.play(FadeOut(task_block_data), FadeOut(efficiency_text))
        self.wait(0.5)
        self.play(Transform(task_block_model, Text("Training-Free Search").scale(0.8)))
        self.wait(1)