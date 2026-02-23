from manim import *

class Concept01BorderOptimization(Scene):
    def construct(self):
        # 1. Setup 4x4 grid of squares
        rows, cols = 4, 4
        squares = VGroup()
        for r in range(rows):
            for c in range(cols):
                sq = Square(side_length=0.9)
                # Position squares manually to avoid arrange_in_grid if restricted
                sq.move_to([c * 1.0 - 1.5, 1.5 - r * 1.0, 0])
                # Initial state: left half RED, right half BLUE
                initial_color = RED if c < 2 else BLUE
                sq.set_fill(initial_color, opacity=1.0)
                sq.set_stroke(WHITE, width=2)
                squares.add(sq)
        
        # 2. Add labels and counter
        # Using Text instead of MathTex/Integer for maximum compatibility
        formula = Text("B = Sum [Different Neighbor Colors]", font_size=24).to_edge(UP)
        counter_label = Text("Border Count: ", font_size=24).to_edge(DOWN).shift(LEFT * 0.5)
        # We will update this Text object manually
        counter_value_mob = Text("0", font_size=24).next_to(counter_label, RIGHT)
        
        self.add(squares, formula, counter_label, counter_value_mob)

        # 3. Helper to define border lines and count adjacencies
        def get_border_mobjects():
            lines = VGroup()
            count = 0
            # Check horizontal neighbors (vertical borders)
            for r in range(rows):
                for c in range(cols - 1):
                    s1 = squares[r * cols + c]
                    s2 = squares[r * cols + (c + 1)]
                    if s1.get_fill_color() != s2.get_fill_color():
                        # Vertical line between s1 and s2
                        center = s1.get_center()
                        p1 = center + 0.5 * RIGHT + 0.45 * UP
                        p2 = center + 0.5 * RIGHT + 0.45 * DOWN
                        lines.add(Line(p1, p2, color=GREEN, stroke_width=8))
                        count += 1
            # Check vertical neighbors (horizontal borders)
            for r in range(rows - 1):
                for c in range(cols):
                    s1 = squares[r * cols + c]
                    s2 = squares[(r + 1) * cols + c]
                    if s1.get_fill_color() != s2.get_fill_color():
                        # Horizontal line between s1 and s2
                        center = s1.get_center()
                        p1 = center + 0.5 * DOWN + 0.45 * LEFT
                        p2 = center + 0.5 * DOWN + 0.45 * RIGHT
                        lines.add(Line(p1, p2, color=GREEN, stroke_width=8))
                        count += 1
            return lines, count

        # Initial display of borders
        border_lines, current_count = get_border_mobjects()
        counter_value_mob.become(Text(str(current_count), font_size=24).next_to(counter_label, RIGHT))
        self.add(border_lines)
        self.wait(1)

        # 4. Animate flips to checkerboard
        for r in range(rows):
            for c in range(cols):
                # Checkerboard target color
                target_color = RED if (r + c) % 2 == 0 else BLUE
                sq = squares[r * cols + c]
                
                # Only animate if color needs to change
                if sq.get_fill_color() != target_color:
                    self.play(
                        sq.animate.set_fill(target_color),
                        run_time=0.2
                    )
                    
                    # Refresh border lines and counter after each flip
                    new_border_lines, new_count = get_border_mobjects()
                    self.remove(border_lines)
                    border_lines = new_border_lines
                    self.add(border_lines)
                    
                    # Refresh counter text
                    new_counter_text = Text(str(new_count), font_size=24).next_to(counter_label, RIGHT)
                    counter_value_mob.become(new_counter_text)
                    self.wait(0.1)

        self.wait(2)