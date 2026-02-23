from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # Formula at the bottom
        formula = MathTex(
            r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)",
            font_size=36
        ).to_edge(DOWN, buff=0.7)

        # 1. Central 'Parent' node
        parent_circle = Circle(radius=0.6, color=BLUE, fill_opacity=0.3)
        parent_label = Text("Parent", font_size=24)
        parent = VGroup(parent_circle, parent_label).shift(UP * 2.5)

        self.add(formula)
        self.play(FadeIn(parent))
        self.wait(0.5)

        # 2. Three 'Child' nodes branching out
        child_nodes = VGroup(*[
            VGroup(
                Circle(radius=0.5, color=GREEN, fill_opacity=0.3),
                Text(f"Child {i+1}", font_size=20)
            ) for i in range(3)
        ]).arrange(RIGHT, buff=1.5).shift(UP * 0.5)

        lines = VGroup(*[
            Line(parent.get_bottom(), child.get_top(), color=GRAY)
            for child in child_nodes
        ])

        # 3. Manual Bar Charts (to avoid BarChart dependency)
        # Each chart has a frame and a bar that will grow
        bars = VGroup()
        for i in range(3):
            # A container box for the win rate
            frame = Rectangle(height=1.5, width=0.6, color=WHITE, stroke_width=2)
            # The actual bar (initial height small but non-zero)
            fill = Rectangle(height=0.05, width=0.5, color=GREEN, fill_opacity=0.8, stroke_width=0)
            # Align fill to the bottom of the frame
            fill.move_to(frame.get_bottom(), aligned_edge=DOWN).shift(UP * 0.05)
            chart = VGroup(frame, fill).next_to(child_nodes[i], DOWN, buff=0.4)
            bars.add(chart)

        self.play(Create(lines), FadeIn(child_nodes))
        self.play(FadeIn(bars))
        self.wait(0.5)

        # 4. Animate bars growing to different heights
        # Target heights scaled relative to the 1.5 height frame
        target_heights = [0.75, 0.45, 1.35]
        
        self.play(
            bars[0][1].animate.stretch_to_fit_height(target_heights[0], about_edge=DOWN),
            bars[1][1].animate.stretch_to_fit_height(target_heights[1], about_edge=DOWN),
            bars[2][1].animate.stretch_to_fit_height(target_heights[2], about_edge=DOWN),
            run_time=2
        )
        self.wait(1)

        # 5. Highlight the child with the highest bar (Child 3) in gold
        self.play(
            bars[2].animate.set_color(GOLD),
            child_nodes[2].animate.set_color(GOLD),
        )
        self.wait(1)

        # 6. Fade out old parent and others, move gold child to the center
        others = VGroup(parent, lines, child_nodes[0], child_nodes[1], bars[0], bars[1])
        
        self.play(
            FadeOut(others),
            FadeOut(bars[2]),
            child_nodes[2].animate.move_to(parent.get_center())
        )
        
        # 7. Designate the new Parent to show the start of the next cycle
        new_label = Text("New Parent", font_size=24, color=GOLD).next_to(child_nodes[2], UP)
        self.play(Write(new_label))
        
        self.wait(2)