from manim import *

class Concept03PseudoExecutionHandoff(Scene):
    def construct(self):
        # 1. Setup Elements
        # Formula at the top
        formula = MathTex(r"s_i^m = \mathrm{PD}(R, \mathcal{A}_m, \mathbf{p}_i, O_i^d)").to_edge(UP, buff=0.5)
        
        # Data Agent Section (Top Half)
        data_label = Text("Data Agent (A_d)", font_size=24).shift(UP * 2 + LEFT * 4)
        data_block = RoundedRectangle(corner_radius=0.1, width=3, height=1.2, color=BLUE).shift(UP * 2 + LEFT * 0.5)
        data_text = Text("Pseudo-Analysis", font_size=18).move_to(data_block)
        
        # Model Agent Section (Bottom Half)
        model_label = Text("Model Agent (A_m)", font_size=24).shift(DOWN * 1 + LEFT * 4)
        task_block = RoundedRectangle(corner_radius=0.1, width=3, height=1.2, color=GREY).shift(DOWN * 1 + LEFT * 0.5)
        task_text = Text("Sub-tasks (s_m)", font_size=18).move_to(task_block)
        
        # Search Efficiency Bar (Bottom)
        bar_bg = Rectangle(width=5, height=0.3, color=WHITE).to_edge(DOWN, buff=1.2)
        bar_fill = Rectangle(width=0.01, height=0.3, fill_color=GREEN, fill_opacity=0.8, stroke_width=0).align_to(bar_bg, LEFT)
        eff_label = Text("Search Efficiency:", font_size=20).next_to(bar_bg, LEFT, buff=0.3)
        
        # Percentage Texts for manual transition
        p0 = Text("0%", font_size=20).next_to(bar_bg, RIGHT, buff=0.2)
        p50 = Text("50%", font_size=20).move_to(p0)
        p100 = Text("100%", font_size=20).move_to(p0)
        
        # 2. Animation Sequence
        # Initial display
        self.play(
            Write(data_label), Create(data_block), Write(data_text),
            Write(model_label), Create(task_block), Write(task_text),
            Create(bar_bg), Create(bar_fill), Write(eff_label), Write(p0)
        )
        self.wait(0.5)
        
        # Data insight generation
        insight_label = MathTex("O_d", color=YELLOW).scale(1.1).move_to(data_block.get_center())
        self.play(
            data_text.animate.shift(UP * 0.25).scale(0.8),
            FadeIn(insight_label, shift=DOWN * 0.1),
            data_block.animate.set_fill(BLUE, opacity=0.2)
        )
        self.wait(0.3)
        
        # Handoff Arrow
        arrow = Arrow(data_block.get_bottom(), task_block.get_top(), color=YELLOW, buff=0.1)
        self.play(Create(arrow))
        
        # Information traveling and intermediate progress
        self.play(
            insight_label.animate.move_to(task_block.get_center()),
            bar_fill.animate.stretch_to_fit_width(2.5, about_edge=LEFT),
            Transform(p0, p50),
            run_time=1.5
        )
        
        # Final expansion and completion
        self.play(
            task_block.animate.scale(1.15).set_fill(ORANGE, opacity=0.2),
            task_text.animate.shift(UP * 0.3),
            insight_label.animate.shift(DOWN * 0.2),
            bar_fill.animate.stretch_to_fit_width(5, about_edge=LEFT),
            Transform(p0, p100),
            Write(formula),
            run_time=1.5
        )
        
        # Final descriptive text
        narration = Text(
            "Training-free search: Agents estimate performance before execution.", 
            font_size=20
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(narration))
        
        self.wait(2)