from manim import *

class PseudoExecutionHandoff(Scene):
    def construct(self):
        # Create agents and blocks
        data_agent = Text("Data Agent (A_d)").to_edge(UP)
        model_agent = Text("Model Agent (A_m)").next_to(data_agent, DOWN)
        
        data_block = Rectangle(width=4, height=2).next_to(data_agent, DOWN)
        model_task_block = VGroup(Text("Task s_m"), Text("(expands as it receives input)").next_to(model_task_block, DOWN)).next_to(model_agent, DOWN)
        
        # Create arrow and search efficiency bar
        arrow = Arrow(data_block.get_bottom(), model_task_block.get_top()).set_color(BLUE)
        search_efficiency_bar = Rectangle(width=4, height=0.2).next_to(model_task_block, DOWN)
        
        # Transforms
        self.play(Create(data_agent), Create(model_agent))
        self.wait(1)
        self.play(Create(data_block), Write(model_task_block[0]))
        self.wait(1)
        
        # Animation for arrow
        self.play(Create(arrow))
        self.wait(1)
        
        # Expand model task block and update search efficiency bar
        model_task_block[1].set_text("(expands as it receives input)")
        self.play(Transform(model_task_block[1], Text("s_m: " + r"$\mathrm{PD}(R, \mathcal{A}_m, \mathbf{p}_i, O_i^d)$", font_size=20)))
        self.wait(1)
        
        # Update search efficiency bar
        for i in range(int(search_efficiency_bar.width / 0.2)):
            search_efficiency_part = Rectangle(width=0.2, height=search_efficiency_bar.height).next_to(search_efficiency_bar, LEFT)
            self.play(FadeIn(search_efficiency_part))
            self.wait(0.25)
        
        self.wait(1)