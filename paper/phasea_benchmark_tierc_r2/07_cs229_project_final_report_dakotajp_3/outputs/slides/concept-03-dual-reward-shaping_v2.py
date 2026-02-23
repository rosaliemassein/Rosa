from manim import *

class DualRewardShaping(Scene):
    def construct(self):
        self.board = VGroup(*[Dot(color=BLUE) for _ in range(5)])
        self.board.arrange_in_grid(rows=3, cols=2)
        self.board.to_edge(UR)

        target_zone = Circle(color=YELLOW, fill_opacity=0.5)
        target_zone.scale(0.75)
        target_zone.to_edge(DR)

        self.centroid = Dot(color=RED).move_to(self.board.get_center())
        self.add(self.board, target_zone)

        w1 = DecimalNumber(2, color=GREEN).next_to(self.board, UR)
        w2 = DecimalNumber(0.5, color=RED).next_to(self.board, UR)
        self.add(w1, w2)

        w1_label = Text("w1 = 2").next_to(w1, DOWN)
        w2_label = Text("w2 = 0.5").next_to(w2, DOWN)
        self.add(w1_label, w2_label)

        title = Text("Dual Reward Shaping").scale(1.5).to_edge(UP)
        self.add(title)

        line = DashedLine(start=self.centroid.get_center(), end=target_zone.get_center()).set_color(GREEN)
        self.add(line)

        count = DecimalNumber(0, color=BLUE).next_to(self.board, UR)
        self.add(count)

        self.play(Write(title))
        self.wait()

        self.add(self.centroid)
        self.add(w1)
        self.add(w2)
        self.add(w1_label)
        self.add(w2_label)

        for i in range(5):
            piece = Dot(color=BLUE)
            self.board.add(piece)

        self.play(Create(self.board))
        self.wait()

        pieces_in_target = 0
        for _ in range(5):
            piece = self.board[i]
            if piece.get_center()[1] <= target_zone.get_center()[1]:
                pieces_in_target += 1
                piece.set_color(GREEN)
            self.add(piece)
            self.wait(0.5)

        count.set_value(pieces_in_target**2)
        self.add(count)

        centroid = Dot(color=RED).move_to(self.board.get_center())
        self.play(Transform(self.centroid, centroid))
        self.wait()

        distance = target_zone.get_center().get_distance(centroid)
        reward = w2**(1/distance)
        self.add(reward)

        for i in range(5):
            piece = self.board[i]
            if piece.get_center()[1] <= target_zone.get_center()[1]:
                reward += w2**(1/distance)

        self.play(Transform(count, count + DecimalNumber(reward, color=BLUE)))
        self.wait()