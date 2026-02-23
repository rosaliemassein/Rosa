from manim import *

class ConceptScene02OpponentAbstraction(Scene):
    def construct(self):
        # Create the 2-player game board
        n = 3  # For 2 players
        opponent1 = Circle(color=BLUE, fill_opacity=0.5)
        opponent2 = Circle(color=RED, fill_opacity=0.5)
        board_2player = VGroup(opponent1, opponent2).arrange(RIGHT, buff=0.5)
        self.play(Create(board_2player))
        
        # Narration
        text_2player = Text("A 2-player board with two distinct colors:")
        self.play(Write(text_2player), run_time=1)
        
        # Create the 6-player game board
        n = 3  # For 6 players (5 opponents + "Red" layer)
        opponent1 = Circle(color=BLUE, fill_opacity=0.5)
        opponent2 = Circle(color=GREEN, fill_opacity=0.5)
        opponent3 = Circle(color=YELLOW, fill_opacity=0.5)
        opponent4 = Circle(color=RED, fill_opacity=0.5)
        opponent5 = Circle(color=BLACK, fill_opacity=0.5)
        # "Red" layer
        opponent6 = Circle(color=RED, fill_opacity=0.5)
        
        board_6player = VGroup(opponent1, opponent2, opponent3, opponent4, opponent5, opponent6).arrange(RIGHT, buff=0.5)
        self.play(Create(board_6player), run_time=1)
        
        # Narration
        text_6player = Text("A 6-player board with 5 different opponent colors:")
        self.play(Write(text_6player), run_time=1)
        
        # Merge the 5 opponent colors into a single 'Red' intensity
        merge_animation = ReplacementTransform(VGroup(opponent1, opponent2, opponent3, opponent4, opponent5), opponent6)
        self.play(merge_animation, run_time=1)
        
        # Cross-out the individual identities of the opponents
        for opponent in VGroup(opponent1, opponent2, opponent3, opponent4, opponent5):
            self.play(Indicate(opponent), run_time=0.5)
        # Check mark over the unified 'Opponent Layer'
        check_mark = Text("Check")
        check_mark.scale(1.5)
        check_mark.set_color(WHITE)
        check_mark.to_edge(DOWN, buff=1.5)
        
        self.play(Write(check_mark), run_time=1)