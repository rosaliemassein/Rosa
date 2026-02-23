from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # Display the evolution formula at the top
        formula = MathTex(r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)").to_edge(UP)
        self.add(formula)

        # Starting Parent node
        parent_node = Dot(color=BLUE).shift(UP * 1.5)
        parent_label = Text("Parent", font_size=24).next_to(parent_node, UP)
        parent = VGroup(parent_node, parent_label)
        self.play(Create(parent))

        # Simulate two generations of evolution as described in remarks
        for gen in range(2):
            # Children positions relative to the parent
            child_offsets = [LEFT * 3.5 + DOWN * 1.5, DOWN * 1.5, RIGHT * 3.5 + DOWN * 1.5]
            # Define different win rates for each generation to show selection
            win_rates = [0.3, 0.5, 0.8] if gen == 0 else [0.9, 0.4, 0.6]
            
            children = VGroup()
            lines = VGroup()
            
            for i in range(3):
                c_dot = Dot(color=BLUE).move_to(child_offsets[i])
                c_text = Text(f"Child {i+1}", font_size=20).next_to(c_dot, UP)
                child = VGroup(c_dot, c_text)
                line = Line(parent_node.get_center(), c_dot.get_center(), stroke_width=2, stroke_opacity=0.6)
                children.add(child)
                lines.add(line)

            # Animate branching out from the parent
            self.play(Create(lines), FadeIn(children))

            # Create bars for win rates below each child
            bars_bg = VGroup()
            bars_fill = VGroup()
            for i in range(3):
                bg = Rectangle(height=1.2, width=0.5, stroke_color=WHITE, stroke_width=1).next_to(children[i], DOWN, buff=0.4)
                # Initial height is almost zero for growth animation
                fill = Rectangle(height=0.01, width=0.5, fill_opacity=0.8, fill_color=YELLOW, stroke_width=0).align_to(bg, DOWN)
                bars_bg.add(bg)
                bars_fill.add(fill)
            
            self.play(Create(bars_bg))
            # Grow bars to represent different win rates
            self.play(
                bars_fill[0].animate.set_height(win_rates[0] * 1.2, stretch=True, about_edge=DOWN),
                bars_fill[1].animate.set_height(win_rates[1] * 1.2, stretch=True, about_edge=DOWN),
                bars_fill[2].animate.set_height(win_rates[2] * 1.2, stretch=True, about_edge=DOWN),
            )
            self.wait(0.5)

            # Identify the child with the highest win rate
            winner_idx = win_rates.index(max(win_rates))
            winner_highlight = SurroundingRectangle(children[winner_idx], color=GOLD, buff=0.1)
            self.play(Create(winner_highlight), bars_fill[winner_idx].animate.set_color(GOLD))
            self.wait(1)

            # Transition: Winner becomes the new Parent, others fade out
            if gen == 0:
                self.play(
                    FadeOut(parent),
                    FadeOut(lines),
                    FadeOut(bars_bg),
                    FadeOut(bars_fill),
                    FadeOut(winner_highlight),
                    *[FadeOut(children[i]) for i in range(3) if i != winner_idx],
                    children[winner_idx].animate.move_to(UP * 1.5)
                )
                
                # Update parent reference for the next iteration
                new_parent_node = children[winner_idx][0]
                new_label = Text("Parent", font_size=24).next_to(new_parent_node, UP)
                self.play(ReplacementTransform(children[winner_idx][1], new_label))
                
                parent = VGroup(new_parent_node, new_label)
                parent_node = new_parent_node
            else:
                # Highlight final winner
                self.play(Indicate(children[winner_idx], color=GOLD))
                self.wait(2)