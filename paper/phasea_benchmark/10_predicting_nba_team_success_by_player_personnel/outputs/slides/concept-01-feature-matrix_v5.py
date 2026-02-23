from manim import *
import numpy as np

class ConceptMatrix(Scene):
    def construct(self):
        # Fallback constants to avoid undefined identifiers
        PI_VAL = 3.14159265
        DEG = PI_VAL / 180.0
        COLOR_GRAY = "#888888"
        
        # 1. Player Silhouettes (15 players)
        # Using Circle and Square as 'Rectangle' is disallowed
        players = VGroup()
        for _ in range(15):
            head = Circle(radius=0.15, color=COLOR_GRAY, fill_opacity=1)
            # Create a rectangle look by scaling a square
            body = Square(side_length=0.35).scale([1, 1.2, 1])
            body.set_style(fill_color=COLOR_GRAY, fill_opacity=1, stroke_width=0)
            body.next_to(head, DOWN, buff=0.02)
            players.add(VGroup(head, body))
        
        players.arrange(DOWN, buff=0.15).to_edge(LEFT, buff=0.7)
        roster_text = Text("Team Roster (15)", font_size=24).next_to(players, UP)
        
        self.play(FadeIn(players), Write(roster_text))
        self.wait(0.5)

        # 2. Minutes Played Filter
        filter_line = Line(LEFT, RIGHT, color=YELLOW).set_width(1.2)
        filter_line.next_to(players[0], UP, buff=0.1)
        filter_label = Text("Top 10 Filter", color=YELLOW, font_size=18).next_to(filter_line, RIGHT)
        
        self.play(Create(filter_line), Write(filter_label))
        
        # Highlight top 10 players and dim the rest
        self.play(
            filter_line.animate.move_to(players[9].get_center() + [0, -0.25, 0]),
            *[players[i].animate.set_color(BLUE) for i in range(10)],
            *[players[i].animate.set_opacity(0.2) for i in range(10, 15)],
            run_time=1.5
        )
        self.wait(0.5)

        # 3. Create 10x15 Feature Matrix (10 players by 15 stats)
        grid = VGroup()
        for r in range(10):
            # Using Square cells for the matrix
            row = VGroup(*[Square(side_length=0.3, stroke_width=1, color=WHITE) for _ in range(15)]).arrange(RIGHT, buff=0.05)
            grid.add(row)
        grid.arrange(DOWN, buff=0.05).shift(RIGHT * 2)

        # 4. Transition players into the rows
        player_animations = []
        for i in range(10):
            player_animations.append(players[i].animate.scale(0.3).next_to(grid[i], LEFT, buff=0.15))
        
        self.play(
            FadeOut(filter_line),
            FadeOut(filter_label),
            FadeOut(roster_text),
            FadeOut(players[10:]),
            *player_animations,
            Create(grid),
            run_time=2
        )

        # 5. Statistic Labels
        stat_names = ["PTS", "REB", "AST", "STL", "BLK", "TOV", "PF", "FG", "FT", "3P", "ORB", "DRB", "USG", "PER", "PIE"]
        stat_labels = VGroup()
        for i, name in enumerate(stat_names):
            lbl = Text(name, font_size=12).next_to(grid[0][i], UP, buff=0.15).rotate(45 * DEG)
            stat_labels.add(lbl)
        
        # Formula using Text instead of MathTex
        formula = Text("n = m x p", font_size=28).to_corner(UP + RIGHT)
        self.play(Write(stat_labels), Write(formula))

        # 6. Fill grid with varying data intensities
        fill_anims = []
        for row in grid:
            for cell in row:
                random_val = np.random.random()
                fill_anims.append(cell.animate.set_fill(BLUE, opacity=random_val))
        
        self.play(*fill_anims, run_time=1.5)
        self.wait(1)

        # 7. Collapse 2D Grid into 1D Vector (150 elements)
        # Flatten the matrix cells
        flat_cells = VGroup(*[cell for row in grid for cell in row])
        
        # Create a horizontal row of small squares to represent the vector
        vector_container = VGroup(*[
            Square(side_length=0.08, stroke_width=0.5, color=BLUE, fill_opacity=np.random.random())
            for _ in range(150)
        ]).arrange(RIGHT, buff=0.01).to_edge(DOWN, buff=1.2)

        self.play(
            FadeOut(players[:10]),
            FadeOut(stat_labels),
            FadeOut(formula),
            Transform(flat_cells, vector_container),
            grid.animate.set_stroke(opacity=0),
            run_time=2
        )
        
        final_label = Text("150-Element Feature Vector", font_size=24).next_to(vector_container, UP)
        self.play(Write(final_label))
        self.wait(2)