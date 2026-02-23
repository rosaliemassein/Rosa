from manim import *
import numpy as np

class BorderOptimization(Scene):
    def construct(self):
        # 1. UI Setup
        goal_text = Text("Goal: Maximize Border Length (B)", font_size=32).to_edge(UP)
        formula = MathTex(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]", font_size=36).next_to(goal_text, DOWN)
        self.add(goal_text, formula)

        # 2. Create Grid & Initial Colors (Left Half Red, Right Half Blue)
        # 4x4 grid: columns 0-1 are Red, columns 2-3 are Blue
        squares = VGroup(*[
            Square(side_length=1, fill_opacity=1, stroke_width=2, stroke_color=WHITE) 
            for _ in range(16)
        ]).arrange_in_grid(4, 4, buff=0)
        
        for i in range(16):
            col = i % 4
            if col < 2:
                squares[i].set_fill(RED)
            else:
                squares[i].set_fill(BLUE)
        
        self.add(squares)

        # 3. Helper Function for Border Lines
        # A border exists between squares if their colors differ
        def get_border_lines(sq_group):
            lines = VGroup()
            for i in range(16):
                row, col = i // 4, i % 4
                # Check Horizontal Neighbors (Right)
                if col < 3:
                    if not np.array_equal(sq_group[i].get_fill_color(), sq_group[i+1].get_fill_color()):
                        line = Line(
                            sq_group[i].get_corner(UR), 
                            sq_group[i].get_corner(DR), 
                            color=GREEN, stroke_width=12
                        )
                        lines.add(line)
                # Check Vertical Neighbors (Bottom)
                if row < 3:
                    if not np.array_equal(sq_group[i].get_fill_color(), sq_group[i+4].get_fill_color()):
                        line = Line(
                            sq_group[i].get_corner(DL), 
                            sq_group[i].get_corner(DR), 
                            color=GREEN, stroke_width=12
                        )
                        lines.add(line)
            return lines

        # 4. Border Lines with Updater
        border_group = get_border_lines(squares)
        def update_borders(mob_obj):
            new_lines = get_border_lines(squares)
            mob_obj.become(new_lines)
        
        border_group.add_updater(update_borders)
        self.add(border_group)

        # 5. Counter UI with Updater
        counter_label = Text("Border Count B = ", font_size=30).to_edge(RIGHT, buff=1.2).shift(UP * 0.5)
        # Start at initial count (4)
        counter_val = Text("4", font_size=40).next_to(counter_label, RIGHT)
        
        def update_counter(mob_obj):
            count = len(border_group)
            new_text = Text(str(count), font_size=40).next_to(counter_label, RIGHT)
            mob_obj.become(new_text)

        counter_val.add_updater(update_counter)
        self.add(counter_label, counter_val)
        self.wait(1)

        # 6. Animation: Flipping to Checkerboard One by One
        # Pre-calculate RGBs for comparison to avoid redundant object creation
        dummy_red = Square().set_fill(RED)
        dummy_blue = Square().set_fill(BLUE)
        red_rgb = dummy_red.get_fill_color()
        blue_rgb = dummy_blue.get_fill_color()

        for i in range(16):
            row, col = i // 4, i % 4
            # Target for Checkerboard: (row + col) is even -> RED, else BLUE
            target_color = RED if (row + col) % 2 == 0 else BLUE
            target_rgb = red_rgb if (row + col) % 2 == 0 else blue_rgb
            
            # If current color isn't the target, flip it
            if not np.array_equal(squares[i].get_fill_color(), target_rgb):
                self.play(
                    squares[i].animate.set_fill(target_color),
                    run_time=0.25
                )

        # 7. Final State
        self.wait(1)
        final_msg = Text("Optimal State: B = 24", color=YELLOW, font_size=36).to_edge(DOWN)
        self.play(Write(final_msg))
        self.wait(2)