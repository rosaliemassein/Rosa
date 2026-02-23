from manim import *

class ConceptPseudoExecutionHandoff(Scene):
    def construct(self):
        # 1. Background / Setup
        title = Text("Concept: Pseudo-Execution Handoff", font_size=36).to_edge(UP)
        voice_text = Text(
            "The real magic happens during plan execution. We decompose each plan\n"
            "into sub-tasks. The Data Agent performs a 'pseudo-analysis' and\n"
            "hands off insights to the Model Agent.",
            font_size=20,
            line_spacing=1.2
        ).to_edge(DOWN, buff=0.5)

        # Split screen divider
        divider = Line(LEFT * 5, RIGHT * 5, color=GRAY).shift(UP * 0.5)
        
        # 2. Agents Setup
        # Top: Data Agent (A_d)
        data_agent_box = Rectangle(width=3, height=1.5, color=BLUE)
        data_agent_label = MathTex(r"\mathcal{A}_d", color=BLUE).scale(1.2)
        data_agent_group = VGroup(data_agent_box, data_agent_label).shift(UP * 2)
        data_title = Text("Data Agent", font_size=24, color=BLUE).next_to(data_agent_box, LEFT)

        # Bottom: Model Agent (A_m)
        model_agent_box = Rectangle(width=3, height=1.5, color=GREEN)
        model_agent_label = MathTex(r"\mathcal{A}_m", color=GREEN).scale(1.2)
        model_agent_group = VGroup(model_agent_box, model_agent_label).shift(DOWN * 1.5)
        model_title = Text("Model Agent", font_size=24, color=GREEN).next_to(model_agent_box, LEFT)

        # 3. Formula
        formula = MathTex(r"s_i^m = \mathrm{PD}(R, \mathcal{A}_m, \mathbf{p}_i, O_i^d)").scale(0.7)
        formula.to_corner(UR, buff=0.5)

        # 4. Search Efficiency Bar
        efficiency_tracker = ValueTracker(0.1)
        bar_label = Text("Search Efficiency", font_size=20).to_edge(RIGHT, buff=1).shift(UP * 0.5)
        bar_bg = Rectangle(width=3, height=0.3, color=WHITE).next_to(bar_label, DOWN)
        bar_fill = always_redraw(lambda: Rectangle(
            width=max(0.01, efficiency_tracker.get_value() * 3),
            height=0.3,
            fill_color=YELLOW,
            fill_opacity=0.8,
            stroke_width=0
        ).align_to(bar_bg, LEFT))
        efficiency_group = VGroup(bar_label, bar_bg, bar_fill)

        # Initial Animation
        self.play(Write(title))
        self.play(Create(divider), FadeIn(voice_text))
        self.play(
            Create(data_agent_group), 
            Create(model_agent_group),
            Write(data_title),
            Write(model_title)
        )
        self.play(Write(formula), FadeIn(efficiency_group))
        self.wait(1)

        # 5. Pseudo-Analysis: Data Agent outputs O_d
        insights_label = MathTex(r"O_i^d", color=BLUE).move_to(data_agent_group)
        self.play(insights_label.animate.shift(RIGHT * 2.5))
        self.play(Indicate(data_agent_box))
        
        # 6. Handoff: Arrow carries O_d to Model Agent
        handoff_arrow = Arrow(
            data_agent_group.get_bottom(), 
            model_agent_group.get_top(), 
            buff=0.2, 
            color=WHITE
        )
        
        self.play(GrowArrow(handoff_arrow))
        self.play(
            insights_label.animate.move_to(model_agent_group.get_center() + RIGHT * 2),
            efficiency_tracker.animate.set_value(0.6),
            run_time=2
        )

        # 7. Model Agent Expansion (s_m)
        sm_box = Rectangle(width=5, height=2, color=GREEN).move_to(model_agent_group)
        sm_text = MathTex(r"s_i^m", color=GREEN).move_to(sm_box.get_top()).shift(DOWN * 0.3)
        
        self.play(
            ReplacementTransform(model_agent_box, sm_box),
            ReplacementTransform(model_agent_label, sm_text),
            FadeOut(insights_label),
            FadeOut(handoff_arrow),
            efficiency_tracker.animate.set_value(1.0),
            run_time=1.5
        )
        
        # Final Note
        final_note = Text("Training-Free Search: In-context performance estimation", font_size=20, color=YELLOW)
        final_note.move_to(voice_text)
        self.play(FadeOut(voice_text), FadeIn(final_note))
        self.play(Indicate(formula))
        self.wait(3)