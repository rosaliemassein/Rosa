from manim import *

class GeneticWinRateSelection(Scene):
    def construct(self):
        # Create the parent node
        parent = Text("Parent", font_size=24)
        
        # Create three child nodes
        children = [
            Text("Child 1", font_size=24),
            Text("Child 2", font_size=24),
            Text("Child 3", font_size=24)
        ]
        
        # Arrange children around the parent
        parent.to_edge(UL, buff=1)
        for child in children:
            child.next_to(parent, RIGHT, buff=0.5)
        
        # Create a bar chart for each child
        win_rates = [0.7, 0.8, 0.6]
        for i, child in enumerate(children):
            win_rate_text = Text(f"Win Rate: {win_rates[i]:.2f}", font_size=18)
            win_rate_text.next_to(child, DOWN, buff=0.3)
            bar = Rectangle(height=win_rates[i] * 0.5, width=1)
            bar.move_to(win_rate_text)
            self.add(bar, win_rate_text)
        
        # Highlight the child with the highest bar in gold
        gold_child = children[win_rates.index(max(win_rates))]
        self.play(Transform(gold_child, Text("New Parent", color=GOLD, font_size=24)))        
        
        # Fade out the other children
        for child in [child for child in children if child != gold_child]:
            self.play(FadeOut(child))
        
        # Repeat the cycle quickly
        for _ in range(5):
            self.play(Transform(gold_child, Text("New Parent", color=GOLD, font_size=24)), run_time=0.5)        
        
        # Final text and image
        final_text = Text("Genetic selection ensures evolutionary gradient for victory", font_size=24)
        final_text.to_edge(DOWN, buff=1)
        self.add(final_text)
        self.wait()