from manim import *

class Concept04ConstrainedOptimization(Scene):
    def construct(self):
        # 1. Setup Title and Formula
        title = Text("Integer Programming: Assignment Matrix", font_size=24).to_edge(UP)
        formula = MathTex(
            r"\max \sum_{i,j} s_{i,j} x_{i,j} - \sum_{k} P_k \delta_k"
        ).scale(0.7).next_to(title, DOWN)
        
        self.add(title, formula)

        # 2. Manual Matrix Construction (to avoid Matrix/IntegerMatrix identifiers)
        matrix_elements = VGroup()
        # Initial binary data
        vals = [
            "1", "0", "1", "0", "0",
            "0", "1", "0", "0", "1",
            "1", "0", "0", "1", "0",
            "0", "0", "1", "0", "1",
            "1", "1", "0", "0", "0"
        ]
        
        for i in range(25):
            char = MathTex(vals[i]).scale(0.6)
            row = i // 5
            col = i % 5
            # Position elements in a 5x5 grid
            char.move_to(LEFT * 4 + RIGHT * col * 0.6 + DOWN * row * 0.6 + UP * 0.5)
            matrix_elements.add(char)
            
        l_bracket = MathTex(r"[", font_size=90).next_to(matrix_elements, LEFT, buff=0.1)
        r_bracket = MathTex(r"]", font_size=90).next_to(matrix_elements, RIGHT, buff=0.1)
        matrix_group = VGroup(matrix_elements, l_bracket, r_bracket)
        matrix_label = Text("Assignment Matrix", font_size=20).next_to(matrix_group, UP)
        
        self.play(Create(matrix_group), Write(matrix_label))

        # 3. Score Bar (Manual animation without ValueTracker/always_redraw)
        score_label = Text("Expertise Score", font_size=20).move_to(RIGHT * 3 + UP * 1)
        bar_bg = Rectangle(width=3, height=0.4, color=WHITE).next_to(score_label, DOWN)
        # Initial bar at 70%
        bar_fill = Rectangle(
            width=2.1, height=0.35, 
            fill_color=GREEN, fill_opacity=0.8, 
            stroke_width=0
        ).align_to(bar_bg, LEFT)
        score_num = MathTex("70").scale(0.8).next_to(bar_bg, RIGHT)
        
        self.play(Create(bar_bg), Create(bar_fill), Write(score_label), Write(score_num))

        # 4. Constraint Icons
        inst_x = VGroup(Line(UL, DR), Line(UR, DL)).set_color(RED).scale(0.2).move_to(RIGHT * 1.5 + DOWN * 1.5)
        div_tri = Triangle().set_color(BLUE).scale(0.2).move_to(RIGHT * 3 + DOWN * 1.5)
        work_clock = VGroup(Circle(), Line(ORIGIN, UP*0.8), Line(ORIGIN, RIGHT*0.5)).set_color(YELLOW).scale(0.2).move_to(RIGHT * 4.5 + DOWN * 1.5)
        
        icon_labels = VGroup(
            Text("Conflict", font_size=14).next_to(inst_x, DOWN),
            Text("Diversity", font_size=14).next_to(div_tri, DOWN),
            Text("Workload", font_size=14).next_to(work_clock, DOWN)
        )
        self.play(FadeIn(inst_x), FadeIn(div_tri), FadeIn(work_clock), FadeIn(icon_labels))

        # 5. Animation: Shift a value and update score
        # Changing entry at index 1 from '0' to '1'
        new_val_1 = MathTex("1").scale(0.6).move_to(matrix_elements[1])
        
        self.play(
            Transform(matrix_elements[1], new_val_1),
            bar_fill.animate.stretch_to_fit_width(2.5, about_edge=LEFT),
            Transform(score_num, MathTex("83").scale(0.8).next_to(bar_bg, RIGHT))
        )
        self.wait(0.5)

        # 6. Animation: Constraint Violation
        # Highlight row 3 (indices 10 to 14)
        row3_group = VGroup(*[matrix_elements[i] for i in range(10, 15)])
        violation_rect = SurroundingRectangle(row3_group, color=RED, buff=0.1)
        
        # Trigger conflict at index 12
        bad_val = MathTex("1", color=RED).scale(0.6).move_to(matrix_elements[12])
        
        self.play(
            Create(violation_rect),
            Transform(matrix_elements[12], bad_val),
            inst_x.animate.scale(1.3).set_color(WHITE),
            bar_fill.animate.stretch_to_fit_width(0.5, about_edge=LEFT).set_color(RED),
            Transform(score_num, MathTex("15").scale(0.8).next_to(bar_bg, RIGHT))
        )
        self.wait(1)

        # 7. Animation: Resolution / Optimization
        self.play(
            FadeOut(violation_rect),
            matrix_elements[12].animate.set_color(WHITE),
            bar_fill.animate.stretch_to_fit_width(2.8, about_edge=LEFT).set_color(GREEN),
            Transform(score_num, MathTex("94").scale(0.8).next_to(bar_bg, RIGHT)),
            inst_x.animate.scale(1/1.3).set_color(RED)
        )
        
        final_text = Text("Constraints Satisfied: Optimal Score", font_size=24, color=GREEN).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)