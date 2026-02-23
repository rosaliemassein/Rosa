from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # 1. Title and Formula
        title = Text("Genetic Win Rate Selection", font_size=36).to_edge(UP)
        formula = MathTex(r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)", font_size=32).next_to(title, DOWN)
        self.add(title, formula)

        # 2. Parent Node
        parent = VGroup(
            Circle(radius=0.6, color=BLUE, fill_opacity=0.2),
            Text("Parent", font_size=24)
        ).move_to(UP * 1.5)
        
        self.play(FadeIn(parent))
        self.wait(0.5)

        # 3. Child Nodes
        child_positions = [LEFT * 4 + DOWN * 0.5, DOWN * 0.5, RIGHT * 4 + DOWN * 0.5]
        children = VGroup()
        arrows = VGroup()
        
        for i, pos in enumerate(child_positions):
            child = VGroup(
                Circle(radius=0.5, color=WHITE, fill_opacity=0.1),
                Text(f"Child {i+1}", font_size=20)
            ).move_to(pos)
            arrow = Arrow(parent.get_bottom(), child.get_top(), buff=0.1, color=GRAY)
            children.add(child)
            arrows.add(arrow)

        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2),
            LaggedStart(*[FadeIn(c) for c in children], lag_ratio=0.2)
        )

        # 4. Bar Charts (Win Rates)
        win_rates = [0.4, 0.85, 0.55] # Child 2 is the winner
        bars = VGroup()
        labels = VGroup()
        bar_containers = VGroup()

        for i, child in enumerate(children):
            # Container for the bar
            container = Rectangle(height=2, width=0.8, color=WHITE, stroke_width=1).next_to(child, DOWN, buff=0.4)
            # The actual bar (start small)
            bar = Rectangle(height=0.01, width=0.7, color=BLUE, fill_opacity=0.8, stroke_width=0).move_to(container.get_bottom(), aligned_edge=DOWN)
            label = Text("Win Rate", font_size=16).next_to(container, DOWN, buff=0.1)
            
            bars.add(bar)
            labels.add(label)
            bar_containers.add(container)

        self.play(FadeIn(bar_containers), FadeIn(labels))
        
        # Animate bars growing to different heights
        self.play(
            bars[0].animate.stretch_to_fit_height(win_rates[0] * 2).move_to(bar_containers[0].get_bottom(), aligned_edge=DOWN),
            bars[1].animate.stretch_to_fit_height(win_rates[1] * 2).move_to(bar_containers[1].get_bottom(), aligned_edge=DOWN).set_color(YELLOW),
            bars[2].animate.stretch_to_fit_height(win_rates[2] * 2).move_to(bar_containers[2].get_bottom(), aligned_edge=DOWN),
            run_time=2
        )
        self.wait(1)

        # 5. Highlight the winner (Child 2)
        winner_index = 1
        winner_rect = SurroundingRectangle(children[winner_index], color=GOLD, buff=0.1)
        self.play(Create(winner_rect), children[winner_index].animate.set_color(GOLD))
        self.wait(1)

        # 6. Fade out others and evolve
        others = VGroup(
            parent, arrows, 
            children[0], children[2], 
            bar_containers, bars[0], bars[2], labels, 
            winner_rect
        )
        
        # Group the winner parts to move them
        winner_group = VGroup(children[winner_index], bars[winner_index])

        self.play(FadeOut(others))
        self.play(winner_group.animate.move_to(UP * 1.5))
        
        # Transform winning child into the new Parent
        new_parent_label = Text("New Parent", font_size=24, color=GOLD).move_to(winner_group[0].get_center())
        self.play(Transform(winner_group[0], new_parent_label))
        self.wait(1)

        # 7. Final message
        final_text = Text("Evolutionary Gradient achieved.", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait(2)