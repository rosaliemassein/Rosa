from manim import *
import random

class GeneticWinRateSelection(Scene):
    def construct(self):
        # 1. Narration and Formula
        voice_text_1 = Text(
            "Standard training minimizes mathematical error,\nbut that doesn't always lead to more wins.", 
            font_size=24
        ).to_edge(UP)
        
        formula = MathTex(
            r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)", 
            font_size=36
        ).next_to(voice_text_1, DOWN)
        
        self.play(Write(voice_text_1))
        self.play(Write(formula))
        self.wait(1)

        # 2. Initial Parent
        parent_point = ORIGIN
        parent = Dot(color=BLUE, radius=0.2).move_to(parent_point)
        parent_label = Text("Parent", font_size=18).next_to(parent, UP)
        self.play(Create(parent), Write(parent_label))
        
        # 3. Evolution Cycle (Repeat to show evolution)
        for cycle in range(2):
            # Create three 'Child' nodes branching out
            child_targets = [
                parent_point + LEFT * 3 + DOWN * 2, 
                parent_point + DOWN * 2, 
                parent_point + RIGHT * 3 + DOWN * 2
            ]
            
            children = VGroup()
            lines = VGroup()
            
            for target in child_targets:
                child = Dot(color=RED, radius=0.15).move_to(parent.get_center())
                line = Line(parent.get_center(), target, stroke_width=2, color=GRAY)
                children.add(child)
                lines.add(line)
            
            self.play(
                AnimationGroup(
                    *[Create(line) for line in lines],
                    *[child.animate.move_to(target) for child, target in zip(children, child_targets)],
                    lag_ratio=0.1
                )
            )

            # Below each child, create a BarChart (using Rectangles for win rate)
            # win_rates: heights for the bars
            win_rates_vals = [random.uniform(0.5, 1.5) for _ in range(3)]
            max_val_index = win_rates_vals.index(max(win_rates_vals))
            
            bars = VGroup()
            bar_labels = VGroup()
            for i, height in enumerate(win_rates_vals):
                bar = Rectangle(
                    width=0.5, 
                    height=height, 
                    fill_opacity=0.8, 
                    color=BLUE, 
                    stroke_width=1
                )
                bar.next_to(children[i], DOWN, buff=0.2)
                # Align the bottom of the bar with the child's position offset
                bar.shift(UP * height / 2) 
                
                label = Text("Win Rate", font_size=12).next_to(bar, DOWN, buff=0.1)
                bars.add(bar)
                bar_labels.add(label)

            self.play(
                *[Create(bar) for bar in bars],
                *[Write(lbl) for lbl in bar_labels]
            )
            self.wait(0.5)

            # Highlight the child with the highest bar in gold
            winner_child = children[max_val_index]
            winner_bar = bars[max_val_index]
            
            self.play(
                winner_child.animate.set_color(GOLD).scale(1.4),
                winner_bar.animate.set_color(GOLD),
                run_time=0.6
            )
            self.wait(0.5)

            # Fade out the parent and other children
            others = VGroup(
                parent, 
                parent_label, 
                lines, 
                *[c for i, c in enumerate(children) if i != max_val_index],
                *[b for i, b in enumerate(bars) if i != max_val_index],
                *[l for i, l in enumerate(bar_labels) if i != max_val_index],
                bar_labels[max_val_index],
                winner_bar
            )
            
            # Move the gold child to the center to become the new 'Parent'
            new_parent_label = Text(f"New Parent (Gen {cycle+1})", font_size=18).move_to(UP * 0.5)
            
            self.play(
                FadeOut(others),
                winner_child.animate.move_to(ORIGIN).set_color(BLUE).scale(1/1.4),
                Transform(parent_label, new_parent_label)
            )
            
            # Update current parent state for next loop
            parent = winner_child
            parent_point = ORIGIN
            self.wait(0.5)

        # 4. Final Text/Summary
        self.play(FadeOut(formula), FadeOut(voice_text_1), FadeOut(parent_label))
        
        goal_text = Text(
            "Genetic selection optimizes models directly for victory.", 
            font_size=24, color=GOLD
        ).to_edge(UP)
        
        final_remark = Text(
            "This ensures the model isn't just getting better at math,\nbut better at the game itself.",
            font_size=22
        ).to_edge(DOWN)

        self.play(Write(goal_text))
        self.play(FadeIn(final_remark, shift=UP))
        self.wait(2)