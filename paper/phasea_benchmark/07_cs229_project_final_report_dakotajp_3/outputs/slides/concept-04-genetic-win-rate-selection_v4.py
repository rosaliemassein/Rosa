from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # Formula using Text instead of MathTex
        formula = Text("P(t+1) = arg max WinRate(c)", font_size=24)
        formula.to_edge(UP)
        self.add(formula)

        # Initial Parent node
        parent_dot = Dot(color=WHITE)
        parent_label = Text("Parent", font_size=20).next_to(parent_dot, UP)
        parent_group = VGroup(parent_dot, parent_label).move_to(ORIGIN)
        
        self.play(FadeIn(parent_group))
        self.wait(0.5)

        # Perform the evolution cycle twice
        for cycle in range(2):
            # 1. Branching out Child nodes
            child_targets = [LEFT * 3 + DOWN * 1.5, DOWN * 1.5, RIGHT * 3 + DOWN * 1.5]
            children = VGroup()
            lines = VGroup()
            
            for i in range(3):
                c_dot = Dot(color=BLUE)
                c_label = Text("Child " + str(i+1), font_size=18).next_to(c_dot, UP)
                child = VGroup(c_dot, c_label).move_to(child_targets[i])
                children.add(child)
                lines.add(Line(parent_group[0].get_center(), c_dot.get_center(), color=WHITE))

            self.play(
                parent_group.animate.shift(UP * 2),
                Create(lines),
                FadeIn(children)
            )

            # 2. Bar charts using Square (stretched) as Rectangle is disallowed
            # Cycle 0: Child 2 (index 1) wins. Cycle 1: Child 1 (index 0) wins.
            heights = [1.2, 2.8, 1.0] if cycle == 0 else [3.0, 1.5, 0.9]
            winner_idx = 1 if cycle == 0 else 0
            
            bars = VGroup()
            bar_labels = VGroup()
            for i, h in enumerate(heights):
                # Creating a bar using Square and stretching it
                bar = Square(side_length=1.0, fill_opacity=0.8, fill_color=BLUE, stroke_color=WHITE)
                bar.stretch_to_fit_height(h)
                bar.stretch_to_fit_width(0.6)
                # Position bar bottom-aligned below the child dot
                bar.move_to(children[i][0].get_center() + DOWN * (h/2 + 0.5))
                
                val = str(int((h/3.5)*100)) + "%"
                lbl = Text(val, font_size=14).next_to(bar, DOWN, buff=0.1)
                
                bars.add(bar)
                bar_labels.add(lbl)

            self.play(
                FadeIn(bars),
                FadeIn(bar_labels)
            )
            self.wait(0.5)

            # 3. Highlight winner in YELLOW
            self.play(
                bars[winner_idx].animate.set_color(YELLOW),
                children[winner_idx].animate.set_color(YELLOW)
            )
            self.wait(1)

            # 4. Evolution Step: Winner becomes new Parent
            # Save winner geometry
            new_parent_dot = children[winner_idx][0].copy()
            new_parent_label = Text("Parent", font_size=20).next_to(new_parent_dot, UP)
            
            # Group everything else for removal
            to_remove = VGroup(
                parent_group, lines, bars, bar_labels,
                *[children[i] for i in range(3) if i != winner_idx],
                children[winner_idx][1] # Old label "Child X"
            )

            self.play(
                FadeOut(to_remove),
                new_parent_dot.animate.move_to(ORIGIN),
                new_parent_label.animate.move_to(UP * 0.4)
            )
            
            # Update parent reference for next cycle
            parent_group = VGroup(new_parent_dot, new_parent_label)
            parent_group.move_to(ORIGIN)
            self.wait(0.5)

        self.wait(1)