from manim import *

class PseudoExecutionHandoff(Scene):
    def construct(self):
        # 1. Setup Titles and Text
        # Using Text instead of MathTex and basic colors to ensure compatibility
        text_title = Text("Pseudo-Execution Handoff", font_size=36).to_edge(UP)
        text_goal = Text("Visualizing Information Handoff", font_size=20, color=BLUE).next_to(text_title, DOWN)
        
        # Formula using Text to avoid MathTex restrictions
        formula = Text("s_i^m = PD(R, Am, pi, Od)", font_size=24).to_corner(DOWN + LEFT)

        # 2. Agents
        # Use YELLOW instead of GOLD, GREY instead of GRAY
        data_agent_circ = Circle(radius=0.7, color=YELLOW).shift(UP * 1.5 + LEFT * 3.5)
        data_label = Text("Data Agent", font_size=24).next_to(data_agent_circ, UP)
        data_agent = VGroup(data_agent_circ, data_label)
        
        model_agent_circ = Circle(radius=0.7, color=BLUE).shift(DOWN * 1.5 + LEFT * 3.5)
        model_label = Text("Model Agent", font_size=24).next_to(model_agent_circ, DOWN)
        model_agent = VGroup(model_agent_circ, model_label)

        # 3. Data Insights and Task Blocks
        data_insight = Text("Od", color=YELLOW).move_to(data_agent_circ.get_center())
        model_task = Text("sm", color=BLUE).move_to(model_agent_circ.get_center())
        
        # 4. Search Efficiency Bar
        # Replacing Rectangle with a thick Line for background and a growing Line for fill
        bar_bg = Line(LEFT * 2, RIGHT * 2, color=WHITE, stroke_width=2).shift(RIGHT * 3 + UP * 0.5)
        efficiency_label = Text("Search Efficiency", font_size=24).next_to(bar_bg, UP)
        
        # The fill is a line created from left to right
        bar_fill = Line(
            bar_bg.get_start(), 
            bar_bg.get_end(), 
            color=GREEN, 
            stroke_width=15
        )

        # 5. Animation Sequence
        self.play(Write(text_title), FadeIn(text_goal))
        self.play(FadeIn(data_agent), FadeIn(model_agent))
        self.wait(0.5)

        # Data Agent Processing
        self.play(Write(data_insight))
        self.play(data_agent_circ.animate.set_fill(YELLOW, opacity=0.3))
        
        # The Handoff
        handoff_arrow = Arrow(data_agent_circ.get_bottom(), model_agent_circ.get_top(), buff=0.1)
        self.play(Create(handoff_arrow))
        self.play(data_insight.animate.move_to(model_agent_circ.get_top() + UP * 0.4))
        
        # Model Agent receives and expands
        self.play(
            FadeOut(data_insight),
            model_agent_circ.animate.scale(1.3).set_fill(BLUE, opacity=0.3),
            Write(model_task)
        )
        self.play(model_task.animate.scale(1.5))

        # Training-free search efficiency bar increase
        self.add(bar_bg, efficiency_label)
        self.play(Write(formula))
        
        # Create animates the line from start point to end point
        self.play(
            Create(bar_fill),
            run_time=3
        )

        self.wait(2)