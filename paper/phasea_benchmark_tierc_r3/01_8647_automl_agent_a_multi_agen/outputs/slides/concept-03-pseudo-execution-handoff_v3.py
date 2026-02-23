from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Setup Layout & Titles
        title_data = Tex(r"Data Agent ($A_d$)", color=BLUE).scale(0.8).to_edge(UP, buff=0.5)
        data_block = VGroup(
            Rectangle(width=3, height=1.5, color=BLUE),
            Text("Data Block", font_size=24)
        ).next_to(title_data, DOWN, buff=0.5)

        title_model = Tex(r"Model Agent ($A_m$)", color=RED).scale(0.8).move_to(DOWN * 0.5)
        model_block = VGroup(
            Rectangle(width=3, height=1.5, color=RED),
            Tex(r"s_m", font_size=36)
        ).next_to(title_model, DOWN, buff=0.5)

        formula = MathTex(r"s_i^m = \mathrm{PD}(R, \mathcal{A}_m, \mathbf{p}_i, O_i^d)").scale(0.7).to_edge(DOWN, buff=0.2)

        # 2. Search Efficiency Bar Setup
        efficiency_tracker = ValueTracker(0)
        eff_label = Text("Search Efficiency:", font_size=20).to_edge(LEFT, buff=0.5).shift(UP * 2)
        
        eff_bar_bg = Rectangle(width=2, height=0.3, color=WHITE).next_to(eff_label, RIGHT)
        eff_bar_fill = always_redraw(lambda: 
            Rectangle(
                width=max(0.01, eff_bar_bg.get_width() * efficiency_tracker.get_value()),
                height=eff_bar_bg.get_height(),
                fill_opacity=0.8,
                fill_color=GREEN,
                stroke_width=0
            ).align_to(eff_bar_bg, LEFT)
        )
        eff_percent = always_redraw(lambda:
            DecimalNumber(efficiency_tracker.get_value() * 100, num_decimal_places=0, unit="%", font_size=20)
            .next_to(eff_bar_bg, RIGHT)
        )
        efficiency_group = VGroup(eff_label, eff_bar_bg, eff_bar_fill, eff_percent)

        # 3. Initial Animation: Data Agent Processing
        self.play(FadeIn(title_data), Create(data_block))
        self.wait(1)

        # 4. Hand-off Sequence
        insight_label = MathTex(r"O_d", color=YELLOW).move_to(data_block.get_center())
        arrow = Arrow(data_block.get_bottom(), model_block.get_top(), color=YELLOW, buff=0.1)
        
        self.play(FadeIn(insight_label))
        self.play(
            insight_label.animate.move_to(arrow.get_center() + RIGHT * 0.5),
            Create(arrow),
            FadeIn(title_model),
            Create(model_block)
        )
        self.wait(0.5)

        # 5. Expanding Model Task Block & Efficiency
        self.add(efficiency_group)
        self.play(
            insight_label.animate.move_to(model_block.get_center()),
            efficiency_tracker.animate.set_value(0.6),
            model_block[0].animate.scale(1.3),
            run_time=2
        )
        self.play(FadeOut(insight_label))
        self.play(efficiency_tracker.animate.set_value(1.0), run_time=1)
        
        # 6. Formula and Closing
        self.play(Write(formula))
        self.wait(1)

        # Narration Subtitles (Minimalistic to prevent clutter)
        narration_1 = Text("Pseudo-analysis identifying key characteristics.", font_size=20, color=GRAY).to_edge(DOWN, buff=1.2)
        narration_2 = Text("Model sub-tasks depend on Data insights.", font_size=20, color=GRAY).to_edge(DOWN, buff=1.2)
        
        self.play(Write(narration_1))
        self.wait(2)
        self.play(ReplacementTransform(narration_1, narration_2))
        self.wait(2)
        self.play(FadeOut(narration_2))
        self.wait(1)

        # Final Highlight
        self.play(Indicate(efficiency_group), Indicate(formula))
        self.wait(2)