from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # Data Agent and Model Agent
        data_agent = Text("Data Agent", font_size=32).to_edge(UP)
        model_agent = Text("Model Agent", font_size=32).to_edge(DOWN)

        # Data Block and Insights
        data_block = Rectangle(height=2, width=1.5).next_to(data_agent, DOWN)
        data_insights = Text("O_d (Data Insights)", font_size=24).next_to(data_block, DOWN)

        # arrows
        arrow = Arrow(start=data_insights.get_bottom(), end=model_agent.get_top())

        # task block for Model Agent
        model_task = Text("s_m (Model Task)", font_size=24).next_to(model_agent, DOWN)

        # search efficiency bar
        search_bar = Rectangle(height=0.2, width=4).next_to(model_agent, RIGHT)
        search_bar.set_color(BLUE)

        # animation
        self.play(Create(data_agent), Create(model_agent))
        self.wait(0.5)
        self.play(FadeIn(data_block), Create(data_insights))
        self.wait(0.5)
        self.play(Create(arrow))
        self.wait(0.5)
        transformation = Transform(model_task, model_task.animate.shift(-1 * RIGHT))
        self.play(transformation)
        self.wait(0.5)
        search_efficiency = Text("Search Efficiency", font_size=24).next_to(search_bar, UP)
        self.play(FadeIn(search_efficiency), Create(search_bar))
        
        # Increase search efficiency
        for _ in range(3):
            self.play(Transform(search_bar, search_bar.animate.scale_in_place(1.2)))
            self.wait(0.5)
            self.play(Transform(search_bar, search_bar.animate.scale_in_place(1/1.2)))