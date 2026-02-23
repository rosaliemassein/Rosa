from manim import *

class ConceptAnimation03(Scene):
    def construct(self):
        # 1. Setup - Title and Divider
        title = Text("Pseudo-Execution Handoff").scale(0.8).to_edge(UP)
        # Using a standard Line instead of DashedLine to avoid disallowed identifiers
        divider = Line(LEFT * 7, RIGHT * 7, stroke_width=1, stroke_opacity=0.5).shift(UP * 0.5)
        
        # 2. Data Agent Area (Top)
        data_agent = Circle(radius=0.4, color=GREEN, fill_opacity=1).shift(UP * 2 + LEFT * 3)
        data_label = Text("A_d (Data Agent)").scale(0.5).next_to(data_agent, LEFT)
        
        data_block = Rectangle(width=2, height=1.2, color=RED).shift(UP * 2 + RIGHT * 2)
        data_block_text = Text("Data Block").scale(0.4).move_to(data_block)
        
        # 3. Model Agent Area (Bottom)
        model_agent = Circle(radius=0.4, color=BLUE, fill_opacity=1).shift(DOWN * 1.5 + LEFT * 3)
        model_label = Text("A_m (Model Agent)").scale(0.5).next_to(model_agent, LEFT)
        
        # Initial small task block
        task_block = Rectangle(width=1.0, height=0.6, color=YELLOW).shift(DOWN * 1.5 + RIGHT * 1)
        task_label = Text("s_m").scale(0.5).move_to(task_block)
        
        # 4. Search Efficiency Bar (Right)
        eff_bg = Rectangle(width=0.5, height=3, color=GREY).to_edge(RIGHT, buff=1.5).shift(DOWN * 0.5)
        # Create the bar with a tiny height to start
        eff_bar = Rectangle(width=0.5, height=0.01, color=YELLOW, fill_opacity=1).align_to(eff_bg, DOWN)
        eff_text = Text("Search Efficiency").scale(0.4).next_to(eff_bg, UP)

        # 5. Formula
        formula = MathTex(r"s_i^m = \mathrm{PD}(R, \mathcal{A}_m, \mathbf{p}_i, O_i^d)").scale(0.7).to_edge(DOWN, buff=0.4)

        # ANIMATION SEQUENCE
        
        # Show Agents and Data
        self.add(title, divider)
        self.play(FadeIn(data_agent), FadeIn(data_label), Create(data_block), Write(data_block_text))
        self.wait(0.5)
        
        # Generate Insights (O_d)
        insight = MathTex("O_d").scale(0.8).move_to(data_block.get_center())
        self.play(insight.animate.next_to(data_agent, RIGHT, buff=0.5))
        self.wait(0.5)
        
        # Handoff: Move O_d down to Model Agent area
        self.play(FadeIn(model_agent), FadeIn(model_label), Create(task_block), Write(task_label))
        self.play(insight.animate.move_to(task_block.get_top() + UP * 0.5))
        
        # Model Agent expands task block as it receives insight
        self.play(
            task_block.animate.stretch_to_fit_width(2.5).shift(RIGHT * 0.5),
            task_label.animate.shift(RIGHT * 0.5),
            insight.animate.scale(0.5).move_to(task_block.get_left() + RIGHT * 0.3),
            run_time=1.5
        )
        self.wait(0.5)
        
        # Visualize Training-Free Search (Efficiency Bar)
        self.add(eff_bg, eff_text)
        self.play(FadeIn(eff_bar))
        
        # Animate the bar growing (simulating efficiency increase)
        # Using stretch instead of ValueTracker/always_redraw
        self.play(
            eff_bar.animate.stretch_to_fit_height(2.5, about_edge=DOWN),
            Write(formula),
            run_time=2
        )
        
        # Highlight completion
        self.play(Indicate(formula), eff_bar.animate.set_color(GREEN))
        self.wait(2)