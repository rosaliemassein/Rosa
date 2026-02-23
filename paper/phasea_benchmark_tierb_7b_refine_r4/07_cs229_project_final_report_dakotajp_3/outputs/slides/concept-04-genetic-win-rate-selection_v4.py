from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # Formula display at the bottom
        formula = MathTex(r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)")
        formula.to_edge(DOWN)
        self.add(formula)

        # 1. Create Parent Node
        parent_circle = Circle(radius=0.5, color=BLUE, fill_opacity=0.3)
        parent_label = Text("Parent Model", font_size=24).next_to(parent_circle, UP)
        parent_group = VGroup(parent_circle, parent_label).shift(UP * 2.5)

        # 2. Create Child Nodes
        child_colors = [RED, GREEN, YELLOW]
        children = VGroup(*[
            Circle(radius=0.4, color=color, fill_opacity=0.3)
            for color in child_colors
        ]).arrange(RIGHT, buff=2).shift(ORIGIN)

        child_labels = VGroup(*[
            Text(f"Child {i+1}", font_size=20).next_to(children[i], UP)
            for i in range(3)
        ])

        # Lines connecting parent to children
        lines = VGroup(*[
            Line(parent_circle.get_bottom(), children[i].get_top())
            for i in range(3)
        ])

        # 3. Create Bar Charts (Represented as Rectangles)
        # We'll use heights to represent win rates (0 to 2 units)
        win_heights = [0.7, 1.8, 1.1] 
        bar_frames = VGroup(*[
            Rectangle(width=0.6, height=2, stroke_color=WHITE, stroke_width=2)
            for _ in range(3)
        ])
        for i, frame in enumerate(bar_frames):
            frame.next_to(children[i], DOWN, buff=0.4)

        # Initial small bars to animate growth
        bar_fills = VGroup(*[
            Rectangle(width=0.6, height=0.01, fill_color=child_colors[i], fill_opacity=0.8, stroke_width=0)
            .align_to(bar_frames[i], DOWN)
            for i in range(3)
        ])

        rate_texts = VGroup(*[
            Text(f"{int(win_heights[i]/2*100)}%", font_size=18).next_to(bar_frames[i], DOWN, buff=0.1)
            for i in range(3)
        ])

        # --- ANIMATION ---

        # Step 1: Show Parent and branching children
        self.play(FadeIn(parent_group))
        self.wait(0.5)
        self.play(
            Create(lines),
            Create(children),
            Write(child_labels),
            run_time=1
        )
        self.wait(0.5)

        # Step 2: Animate the win rate bars growing
        self.play(
            Create(bar_frames),
            *[bar_fills[i].animate.stretch_to_fit_height(win_heights[i]).align_to(bar_frames[i], DOWN) 
              for i in range(3)],
            Write(rate_texts),
            run_time=2
        )
        self.wait(1)

        # Step 3: Highlight the winner (Child 2 - Green)
        winner_idx = 1
        gold_highlight = SurroundingRectangle(children[winner_idx], color=GOLD, buff=0.1, stroke_width=6)
        winner_tag = Text("BEST PERFORMANCE", color=GOLD, font_size=24).next_to(gold_highlight, UP, buff=0.5)
        
        self.play(
            Create(gold_highlight),
            Write(winner_tag),
            children[winner_idx].animate.set_fill(GOLD, opacity=0.6).set_color(GOLD),
            bar_fills[winner_idx].animate.set_color(GOLD)
        )
        self.wait(1.5)

        # Step 4: Evolution - Fade out non-winners and move winner to parent position
        others = VGroup(
            parent_group, lines, 
            children[0], children[2], 
            child_labels, rate_texts, 
            bar_frames, bar_fills,
            winner_tag, gold_highlight
        )
        
        # Capture the winner to animate separately
        winner_circle = children[winner_idx]

        self.play(FadeOut(others))
        
        # Step 5: Winner becomes the new Parent
        new_parent_pos = parent_circle.get_center()
        self.play(
            winner_circle.animate.move_to(new_parent_pos).scale(1.25),
            run_time=1.5
        )
        
        final_label = Text("New Generation Parent", font_size=24, color=GOLD).next_to(winner_circle, UP)
        self.play(Write(final_label))
        
        # Quick flash to suggest recurring evolution
        self.play(Flash(winner_circle, color=GOLD, flash_radius=0.7))
        self.wait(2)