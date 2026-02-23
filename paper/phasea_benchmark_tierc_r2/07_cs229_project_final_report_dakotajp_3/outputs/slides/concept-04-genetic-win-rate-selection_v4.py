import numpy as np
from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # 1. Setup Narration and Formula
        voice_text = Text(
            "Evolutionary gradient for victory",
            font_size=24
        ).to_edge(UP)
        
        formula = MathTex(
            r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)",
            font_size=36
        ).next_to(voice_text, DOWN)

        self.play(Write(voice_text), Write(formula))
        self.wait(1)

        # 2. Initial Parent
        parent_node = VGroup(
            Circle(radius=0.4, color=BLUE, fill_opacity=0.5),
            Text("Parent", font_size=20).shift(UP * 0.6)
        ).move_to(UP * 1)

        self.play(Create(parent_node))
        self.wait()

        # 3. Evolution Loop
        for generation in range(2):
            # Create children
            children = VGroup()
            lines = VGroup()
            for i in range(3):
                child = VGroup(
                    Circle(radius=0.3, color=BLUE, fill_opacity=0.3),
                    Text(f"C{i+1}", font_size=18).shift(UP * 0.5)
                )
                child.move_to(DOWN * 0.5 + (i - 1) * 3 * RIGHT)
                line = Line(parent_node.get_center(), child.get_center(), stroke_width=2, color=GRAY)
                children.add(child)
                lines.add(line)

            self.play(
                LaggedStart(*[Create(l) for l in lines], lag_ratio=0.2),
                LaggedStart(*[FadeIn(c) for c in children], lag_ratio=0.2)
            )

            # 4. Bar Charts (Win Rates)
            win_values = [0.4, 0.6, 0.85] if generation == 0 else [0.5, 0.9, 0.6]
            winner_idx = int(np.argmax(win_values))
            
            bars = VGroup()
            labels = VGroup()
            for i, val in enumerate(win_values):
                # Create bar and position it
                bar = Rectangle(
                    height=val * 1.5, 
                    width=0.6, 
                    fill_opacity=0.8, 
                    fill_color=BLUE
                ).next_to(children[i], DOWN, buff=0.2)
                # Ensure the bar grows from the bottom
                bar.shift(UP * bar.height / 2)
                
                label = Text(f"{int(val*100)}%", font_size=16).next_to(bar, DOWN, buff=0.1)
                bars.add(bar)
                labels.add(label)

            # Manually animate growth to avoid GrowFromEdge issues
            self.play(
                LaggedStart(*[FadeIn(b, shift=UP*0.5) for b in bars], lag_ratio=0.3),
                FadeIn(labels)
            )
            self.wait(0.5)

            # 5. Highlight winner in Gold
            self.play(
                bars[winner_idx].animate.set_color(GOLD),
                children[winner_idx][0].animate.set_color(GOLD),
                children[winner_idx][1].animate.set_color(GOLD),
                run_time=0.5
            )
            self.wait(1)

            # 6. Transform winner to new Parent
            others = VGroup()
            for i in range(3):
                if i != winner_idx:
                    others.add(children[i], lines[i], bars[i], labels[i])
            
            # Add previous parent and current winner artifacts to cleanup list
            others.add(parent_node, lines[winner_idx], bars[winner_idx], labels[winner_idx])

            new_parent_pos = UP * 1
            if generation == 0:
                self.play(
                    FadeOut(others),
                    children[winner_idx].animate.move_to(new_parent_pos)
                )
                # Create a fresh parent node for consistency
                parent_node = VGroup(
                    Circle(radius=0.4, color=BLUE, fill_opacity=0.5),
                    Text("Parent", font_size=20).shift(UP * 0.6)
                ).move_to(new_parent_pos)
                self.remove(children[winner_idx])
                self.add(parent_node)
            else:
                self.play(FadeOut(others), children[winner_idx].animate.scale(1.2).move_to(ORIGIN))

        # Final frame
        self.play(FadeOut(voice_text), formula.animate.move_to(UP*2))
        success_text = Text("Optimal Strategy Selected", color=GOLD).next_to(formula, DOWN, buff=1)
        self.play(Write(success_text))
        self.wait(2)