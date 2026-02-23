from manim import *

class ConceptExecutionHandoff(Scene):
    def construct(self):
        # 1. Setup Elements
        # Agents
        data_agent = VGroup(
            Circle(color=BLUE, fill_opacity=0.2),
            Text("Data Agent (Ad)", font_size=24)
        ).arrange(DOWN).to_edge(UP, buff=0.5)

        model_agent = VGroup(
            Circle(color=GREEN, fill_opacity=0.2),
            Text("Model Agent (Am)", font_size=24)
        ).arrange(DOWN).to_edge(DOWN, buff=0.5)

        # Formula
        formula = MathTex(r"s_i^m = \mathrm{PD}(R, \mathcal{A}_m, \mathbf{p}_i, O_i^d)").scale(0.8).to_corner(UL)

        # Data Block
        data_block = Rectangle(color=GREY, width=2, height=1.2, fill_opacity=0.5).next_to(data_agent, LEFT, buff=1)
        data_label = Text("Data Block", font_size=18).move_to(data_block.get_center())
        
        # Insights (O_d)
        o_d = VGroup(
            Rectangle(color=YELLOW, width=1.4, height=0.7, fill_opacity=0.8),
            Text("Insights (Od)", font_size=16, color=BLACK)
        ).move_to(data_agent.get_center())

        # Search Efficiency Bar (Avoid ValueTracker)
        bar_bg = Rectangle(width=4, height=0.4, color=WHITE).to_corner(DR, buff=1)
        bar_fill = Rectangle(width=0.1, height=0.4, color=GREEN, fill_opacity=0.8).align_to(bar_bg, LEFT)
        bar_label = Text("Search Efficiency", font_size=20).next_to(bar_bg, UP)

        # Model Task Block (s_m)
        s_m = Square(side_length=0.4, color=ORANGE, fill_opacity=0.5).move_to(model_agent.get_center())

        # 2. Animation Sequence
        self.add(formula)
        self.play(FadeIn(data_agent), FadeIn(model_agent))
        self.play(Create(data_block), Write(data_label))
        self.wait(0.5)

        # Narration: Data Agent processes data
        narr_text1 = Text("Data Agent performs pseudo-analysis", font_size=20).to_edge(RIGHT).shift(UP * 2)
        self.play(Write(narr_text1))
        self.play(data_block.animate.set_color(BLUE))
        self.play(FadeIn(o_d))
        self.wait(0.5)

        # Narration: Handoff
        self.play(FadeOut(narr_text1))
        narr_text2 = Text("Handing off insights to Model Agent", font_size=20).to_edge(RIGHT).shift(UP)
        self.play(Write(narr_text2))
        
        arrow = Arrow(data_agent.get_bottom(), model_agent.get_top(), buff=0.2)
        self.play(Create(arrow))
        self.play(
            o_d.animate.move_to(model_agent.get_center()).scale(0.5),
            run_time=1.5
        )
        self.play(FadeOut(o_d), FadeOut(arrow))
        
        # Narration: Task expansion & Efficiency
        self.play(FadeOut(narr_text2))
        narr_text3 = Text("Model Agent tasks depend on output", font_size=20).to_edge(RIGHT)
        self.play(Write(narr_text3))
        
        # Show s_m expanding
        self.play(Create(s_m))
        self.play(s_m.animate.scale(4).set_opacity(0.3))
        
        # Search Efficiency Bar increase
        self.play(Create(bar_bg), Create(bar_fill), Write(bar_label))
        # Animate the bar width manually instead of using ValueTracker
        self.play(
            bar_fill.animate.stretch_to_fit_width(3.9, about_edge=LEFT),
            run_time=3
        )
        
        # Final Narration
        self.play(FadeOut(narr_text3))
        final_msg = Text("Training-free search using in-context learning", font_size=18, color=YELLOW).next_to(bar_bg, DOWN, buff=0.4)
        self.play(Write(final_msg))
        self.wait(2)

        # Final Cleanup
        self.play(
            FadeOut(data_agent), FadeOut(model_agent), FadeOut(data_block), 
            FadeOut(data_label), FadeOut(s_m), FadeOut(formula), 
            FadeOut(final_msg), FadeOut(bar_bg), FadeOut(bar_fill), FadeOut(bar_label)
        )
        self.wait(1)