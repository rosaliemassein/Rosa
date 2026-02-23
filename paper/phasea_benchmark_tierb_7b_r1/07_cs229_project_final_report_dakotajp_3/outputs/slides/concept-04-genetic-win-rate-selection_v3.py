from manim import *

class GeneticSelection(Scene):
    def construct(self):
        # 1. Formula Display
        formula = MathTex(r"P_{t+1} = \arg\max_{c \in \text{Children}(P_t)} \text{WinRate}(c)")
        formula.to_edge(UP)
        self.add(formula)

        # 2. Initial Parent
        parent_node = Dot(radius=0.2, color=BLUE).shift(UP * 1.5)
        parent_label = Text("Parent", font_size=24).next_to(parent_node, UP)
        parent = VGroup(parent_node, parent_label)
        
        self.play(FadeIn(parent))
        self.wait(0.5)

        # 3. Children Setup
        child_colors = [GREEN, GREEN, GREEN]
        child_positions = [LEFT * 3 + DOWN * 0.5, DOWN * 0.5, RIGHT * 3 + DOWN * 0.5]
        win_rates = [0.3, 0.9, 0.5] # Middle one is the winner
        
        children = VGroup()
        branches = VGroup()
        bars = VGroup()
        bar_labels = VGroup()

        for i in range(3):
            # Child Node
            child_dot = Dot(radius=0.15, color=child_colors[i]).move_to(child_positions[i])
            child_text = Text(f"Child {i+1}", font_size=20).next_to(child_dot, RIGHT, buff=0.1)
            child = VGroup(child_dot, child_text)
            children.add(child)
            
            # Branching line
            line = Line(parent_node.get_center(), child_dot.get_center(), stroke_width=2, color=GREY)
            branches.add(line)
            
            # Win Rate Bar
            # Using Rectangle to represent win rate
            bar_height = win_rates[i] * 2.5
            bar = Rectangle(
                width=0.6, 
                height=bar_height, 
                fill_opacity=0.8, 
                fill_color=BLUE,
                stroke_color=WHITE
            ).next_to(child_dot, DOWN, buff=0.5)
            # Align bottom to a common ground
            bar.shift(DOWN * (1.25 - bar_height/2))
            bars.add(bar)
            
            label = Text(f"{int(win_rates[i]*100)}%", font_size=16).next_to(bar, DOWN, buff=0.1)
            bar_labels.add(label)

        # 4. Animation Sequence
        self.play(Create(branches))
        self.play(FadeIn(children))
        self.wait(0.5)
        
        # Animate bars appearing (using FadeIn with shift to simulate growth)
        self.play(
            *[FadeIn(bar, shift=UP) for bar in bars],
            FadeIn(bar_labels)
        )
        self.wait(1)

        # 5. Highlight the winner (index 1)
        winner_idx = 1
        winner_highlight = SurroundingRectangle(VGroup(children[winner_idx], bars[winner_idx]), color=YELLOW, buff=0.2)
        
        self.play(
            Create(winner_highlight),
            bars[winner_idx].animate.set_color(YELLOW),
            children[winner_idx][0].animate.set_color(YELLOW)
        )
        self.wait(1)

        # 6. Evolutionary Transition
        # Group everything that needs to disappear
        to_fade = VGroup(
            parent,
            branches,
            winner_highlight,
            bar_labels,
            *[children[i] for i in range(3) if i != winner_idx],
            *[bars[i] for i in range(3) if i != winner_idx]
        )

        # The winning child moves to become the new parent
        new_parent_pos = UP * 1.5
        
        self.play(
            FadeOut(to_fade),
            FadeOut(bars[winner_idx]),
            children[winner_idx].animate.move_to(new_parent_pos)
        )
        
        # Update label to "New Parent"
        new_label = Text("New Parent", font_size=24, color=YELLOW).next_to(children[winner_idx], UP)
        self.play(Transform(children[winner_idx][1], new_label))
        
        self.wait(1)

        # 7. Final emphasis
        success_text = Text("Evolutionary Selection Complete", font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(success_text))
        self.wait(2)