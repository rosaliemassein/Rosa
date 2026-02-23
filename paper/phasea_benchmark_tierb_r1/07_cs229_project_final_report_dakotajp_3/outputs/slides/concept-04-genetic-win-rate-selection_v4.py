from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # 1. Title and Formula
        title = Text("Genetic Win Rate Selection", font_size=36).to_edge(UP)
        formula = MathTex(r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)")
        formula.next_to(title, DOWN, buff=0.2)
        self.add(title, formula)

        # 2. Initial Parent Node
        parent_node = VGroup(
            Circle(radius=0.5, color=BLUE, fill_opacity=0.2),
            Text("Parent", font_size=24)
        ).move_to(UP * 1.5)
        
        self.play(FadeIn(parent_node))
        self.wait(0.5)

        # Evolutionary cycles (Repeated twice to show evolution)
        for gen in range(2):
            # 3. Branching Children Nodes
            children_nodes = VGroup(*[
                VGroup(
                    Circle(radius=0.4, color=WHITE, fill_opacity=0.1),
                    Text(f"Child {j+1}", font_size=20)
                ) for j in range(3)
            ]).arrange(RIGHT, buff=1.5).move_to(ORIGIN)
            
            # Draw lines from Parent to Children
            lines = VGroup(*[
                Line(parent_node.get_bottom(), child.get_top(), stroke_width=2, color=GRAY)
                for child in children_nodes
            ])

            self.play(
                Create(lines),
                FadeIn(children_nodes),
                run_time=1
            )

            # 4. Bar Charts representing Win Rate
            # Pre-set win rates: 1st gen child 2 wins, 2nd gen child 1 wins
            if gen == 0:
                win_rates = [0.35, 0.82, 0.55]
                winner_idx = 1
            else:
                win_rates = [0.92, 0.65, 0.78]
                winner_idx = 0

            bars = VGroup()
            labels = VGroup()
            for j, wr in enumerate(win_rates):
                # Create a bar below each child node
                bar = Rectangle(
                    width=0.6, 
                    height=wr * 2, 
                    fill_opacity=0.8, 
                    color=BLUE
                ).next_to(children_nodes[j], DOWN, buff=0.3)
                # Create percentage labels
                lbl = Text(f"{int(wr*100)}%", font_size=16).next_to(bar, DOWN, buff=0.1)
                bars.add(bar)
                labels.add(lbl)

            self.play(
                LaggedStart(*[FadeIn(b, shift=UP) for b in bars], lag_ratio=0.2),
                FadeIn(labels),
                run_time=1.5
            )
            self.wait(0.5)

            # 5. Highlight the child with the highest win rate
            self.play(
                bars[winner_idx].animate.set_color(GOLD),
                children_nodes[winner_idx].animate.set_color(GOLD),
                run_time=0.8
            )
            self.wait(1)

            # 6. Evolutionary Transition: Move winner to center to become new parent
            losers = VGroup(
                *[children_nodes[j] for j in range(3) if j != winner_idx],
                *[bars[j] for j in range(3) if j != winner_idx],
                *[labels[j] for j in range(3) if j != winner_idx],
                lines,
                parent_node
            )
            
            winner_node = children_nodes[winner_idx]
            winner_bar = bars[winner_idx]
            winner_label = labels[winner_idx]
            
            new_parent_label = Text("Parent", font_size=24).move_to(UP * 1.5)

            self.play(
                FadeOut(losers),
                winner_node.animate.move_to(UP * 1.5),
                FadeOut(winner_bar),
                FadeOut(winner_label),
                run_time=1.2
            )
            
            self.play(
                Transform(winner_node[1], new_parent_label),
                winner_node[0].animate.set_color(BLUE),
                run_time=0.5
            )
            
            # Update the reference for the next cycle
            parent_node = winner_node
            self.wait(0.5)

        self.wait(2)