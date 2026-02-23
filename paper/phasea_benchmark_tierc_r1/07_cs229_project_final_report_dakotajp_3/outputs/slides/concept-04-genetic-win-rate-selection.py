from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # Title and Voice
        title = Text("Concept 04 - Genetic Win Rate Selection", font_size=24, color=WHITE)
        narration = Text("According to the concept slide...", font_size=18, color=BLUE)
        self.play(Create(title), Write(narration))
        self.wait()

        # Parent Node
        parent = Circle(radius=0.5, color=YELLOW).move_to([-3, 2, 0])
        self.play(Create(parent))
        
        # Children Nodes
        children = [Circle(radius=0.5, color=GREEN) for _ in range(3)]
        first_child = children[0].move_to([-1, 2, 0])
        second_child = children[1].move_to([1, 2, 0])
        third_child = children[2].move_to([-2.5, -1, 0])
        self.play(Create(first_child), Create(second_child), Create(third_child))

        # Win Rate Bars
        chart_height = 1.2
        win_rates = [0.4, 0.75, 0.6]
        bar_width = 1
        for i, child in enumerate(children):
            bar_height = chart_height * win_rates[i]
            bar = Rectangle(width=bar_width, height=bar_height, color=RED)
            bar.move_to([0, chart_height / 2 + i * (chart_height + 1), 0])
            self.play(Create(bar))
        
        # Highlighting the best child
        max_win_rate = max(win_rates)
        for i, win_rate in enumerate(win_rates):
            if win_rate == max_win_rate:
                self.play(Transform(bar, Rectangle(width=bar_width, height=bar_height * 1.2, color=GOLD)))

        # Updating the parent node
        self.play(Transform(parent, Circle(radius=0.5, color=YELLOW).move_to([1.5, 2, 0])))
        first_child = first_child.move_to([-1.8, 2, 0])
        second_child = second_child.move_to([1.8, 2, 0])
        third_child = third_child.move_to([-2.3, -1, 0])

        # Repeat cycle
        for _ in range(2):
            self.wait(1)
            self.play(Transform(parent, Circle(radius=0.5, color=YELLOW).move_to([-3, 2, 0])))
            self.wait(1)
            for i, child in enumerate(children):
                self.play(Create(bar), Transform(first_child, Rectangle(width=bar_width, height=bar_height * 1.2, color=GOLD)))

        self.wait()