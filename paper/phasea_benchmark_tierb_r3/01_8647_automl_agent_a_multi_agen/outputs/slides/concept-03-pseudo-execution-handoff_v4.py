from manim import *

class ConceptExecutionHandoff(Scene):
    def construct(self):
        # 1. Setup Layout and Titles
        title = Text("Pseudo-Execution Handoff", font_size=32).to_edge(UP)
        divider = Line(LEFT * 7, RIGHT * 7).shift(UP * 0.5)
        
        # Agents
        data_agent = VGroup(
            Circle(radius=0.5, color=YELLOW, fill_opacity=0.3),
            Text("Data Agent (A_d)", font_size=20)
        ).arrange(DOWN, buff=0.2).shift(UP * 2 + LEFT * 4)
        
        model_agent = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.3),
            Text("Model Agent (A_m)", font_size=20)
        ).arrange(DOWN, buff=0.2).shift(DOWN * 1.5 + LEFT * 4)
        
        # Formula
        formula = MathTex(
            "s_i^m = \\mathrm{PD}(R, \\mathcal{A}_m, \\mathbf{p}_i, O_i^d)",
            font_size=34
        ).to_edge(RIGHT, buff=1).shift(UP * 1.5)
        
        # Efficiency Bar Components (Static replacements for updaters)
        eff_label = Text("Search Efficiency", font_size=22).shift(DOWN * 3 + LEFT * 3)
        eff_bg = Rectangle(width=4, height=0.3, color=GRAY, stroke_width=1).next_to(eff_label, RIGHT, buff=0.5)
        eff_fill = Rectangle(width=0.1, height=0.3, fill_color=GREEN, fill_opacity=0.8, stroke_width=0)
        eff_fill.align_to(eff_bg, LEFT)

        # 2. Initial Appearance
        self.add(title, divider)
        self.play(FadeIn(data_agent), FadeIn(model_agent))
        self.play(Write(formula))
        self.play(Create(eff_bg), Create(eff_fill), Write(eff_label))
        self.wait(1)

        # 3. Data Agent pseudo-analysis (Generating O_d)
        data_box = Square(side_length=0.8, color=YELLOW).next_to(data_agent, RIGHT, buff=1)
        data_box_label = Text("Data", font_size=16).move_to(data_box)
        
        self.play(Create(data_box), Write(data_box_label))
        
        insights = MathTex("O_i^d", color=YELLOW, font_size=36).move_to(data_box.get_center())
        insights_text = Text("Insights", font_size=16, color=YELLOW).next_to(insights, UP, buff=0.1)
        
        self.play(
            ReplacementTransform(data_box, insights),
            ReplacementTransform(data_box_label, insights_text)
        )
        self.wait(0.5)

        # 4. Information Handoff Arrow
        handoff_arrow = Arrow(insights.get_bottom(), model_agent.get_top(), color=WHITE, buff=0.1)
        
        self.play(GrowArrow(handoff_arrow))
        self.wait(0.5)

        # 5. Model Agent Task (s_m) Initialization
        task_box = Rectangle(width=1.2, height=0.7, color=BLUE).next_to(model_agent, RIGHT, buff=1)
        task_label = MathTex("s_i^m", font_size=28).move_to(task_box)

        # Move insights to task location
        self.play(
            insights.animate.move_to(task_box.get_center()),
            FadeOut(insights_text),
            FadeOut(handoff_arrow),
            run_time=1.2
        )
        
        self.play(
            ReplacementTransform(insights, task_box),
            Write(task_label)
        )

        # 6. Expansion and Efficiency Increase
        # Instead of ValueTracker, we use direct transformations
        expanded_task_box = Rectangle(width=4.0, height=1.0, color=BLUE).move_to(task_box).shift(RIGHT * 1.2)
        expanded_task_text = Text("Training-Free Sub-tasks Deployed", font_size=18).move_to(expanded_task_box)
        
        # Animate the bar growth and task expansion together
        self.play(
            Transform(task_box, expanded_task_box),
            Transform(task_label, expanded_task_text),
            eff_fill.animate.stretch_to_fit_width(3.8).align_to(eff_bg, LEFT),
            run_time=2
        )

        # 7. Final highlight on the formula dependency
        highlight = SurroundingRectangle(formula[0][-3:], color=YELLOW, buff=0.1)
        dependency_text = Text("In-Context Dependency", font_size=14, color=YELLOW).next_to(highlight, DOWN)
        
        self.play(Create(highlight), Write(dependency_text))
        self.wait(2)