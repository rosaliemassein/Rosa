from manim import *

class OpponentAbstraction(Scene):
    def construct(self):
        # Initialize 2-player board
        player1 = Circle().set_color(BLUE).scale(0.5)
        player2 = Circle().set_color(RED).scale(0.5)
        board_2p = VGroup(player1, player2).arrange(RIGHT, buff=0.5)
        board_2p.to_edge(UP)

        # Initialize 6-player board
        players_6p = [Circle().set_color(i).scale(0.5) for i in [BLUE, GREEN, RED, YELLOW, PURPLE]]
        board_6p = VGroup(*players_6p).arrange(RIGHT, buff=0.5)
        board_6p.to_edge(UP)

        # Animation of cross-out and checkmark
        for player in players_6p:
            self.play(FadeOut(player))
            self.wait(0.2)

        checkmark = MathTex(r"\checkmark").set_color(GREEN).scale(1.5)
        checkmark.to_edge(UP)

        # Transform 6-player board into single 'Red' opponent layer
        self.play(Transform(board_2p, MathTex(r"O").set_color(RED).scale(1.5)))
        self.play(Transform(board_6p, checkmark))

        # Narration
        text = Text("The real secret to generalization lies in how we treat the competition.").scale(0.7)
        text.next_to(checkmark, DOWN)
        self.play(FadeIn(text))
        self.wait(2)

        faded_text = Text("The real secret to generalization lies in how we treat the competition.", color=WHITE).scale(0.7)
        faded_text.next_to(checkmark, DOWN)
        self.play(Transform(text, faded_text))
        self.wait(2)

        text = Text("Instead of giving every opponent their own channel, we lump them all into a single 'opponent layer'.").scale(0.7)
        text.next_to(checkmark, DOWN)
        self.play(FadeIn(text))
        self.wait(2)

        faded_text = Text("Instead of giving every opponent their own channel, we lump them all into a single 'opponent layer'.", color=WHITE).scale(0.7)
        faded_text.next_to(checkmark, DOWN)
        self.play(Transform(text, faded_text))
        self.wait(2)

        text = Text("This makes the 6-player game look structurally identical to the 2-player game.").scale(0.7)
        text.next_to(checkmark, DOWN)
        self.play(FadeIn(text))
        self.wait(2)

        faded_text = Text("This makes the 6-player game look structurally identical to the 2-player game.", color=WHITE).scale(0.7)
        faded_text.next_to(checkmark, DOWN)
        self.play(Transform(text, faded_text))
        self.wait(2)

        text = Text("Because the network only sees 'me' versus 'the field', a strategy learned against one opponent naturally scales to five without changing the model's architecture.").scale(0.7)
        text.next_to(checkmark, DOWN)
        self.play(FadeIn(text))
        self.wait(2)

        faded_text = Text("Because the network only sees 'me' versus 'the field', a strategy learned against one opponent naturally scales to five without changing the model's architecture.", color=WHITE).scale(0.7)
        faded_text.next_to(checkmark, DOWN)
        self.play(Transform(text, faded_text))
        self.wait(2)

        text = Text("Explain the encoding trick that allows a model trained on 2 players to function in 3, 4, or 6 player games.").scale(0.7)
        text.next_to(checkmark, DOWN)
        self.play(FadeIn(text))
        self.wait(2)

        faded_text = Text("Explain the encoding trick that allows a model trained on 2 players to function in 3, 4, or 6 player games.", color=WHITE).scale(0.7)
        faded_text.next_to(checkmark, DOWN)
        self.play(Transform(text, faded_text))
        self.wait(2)

        self.wait()