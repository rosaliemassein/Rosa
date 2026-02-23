from manim import *

class ConceptOptimization(Scene):
    def construct(self):
        # 1. Setup Grid and Initial State
        squares = VGroup(*[Square(side_length=1.0, stroke_color=WHITE, stroke_width=2) for _ in range(16)])
        squares.arrange_in_grid(rows=4, cols=4, buff=0)
        squares.shift(LEFT * 2.5)

        # Initial coloring: Left half (columns 0,1) Red, Right half (columns 2,3) Blue
        for i in range(16):
            col = i % 4
            if col < 2:
                squares[i].set_fill(RED, opacity=1)
            else:
                squares[i].set_fill(BLUE, opacity=1)
        
        self.add(squares)

        # 2. Border and Adjacency Calculation Logic
        def get_adjacencies_and_lines():
            lines = VGroup()
            count = 0
            # Vertical borders (check horizontal neighbors)
            for r in range(4):
                for c in range(3):
                    idx1 = r * 4 + c
                    idx2 = r * 4 + c + 1
                    s1 = squares[idx1]
                    s2 = squares[idx2]
                    if s1.get_fill_color() != s2.get_fill_color():
                        count += 1
                        lines.add(Line(
                            s1.get_corner(UR), s1.get_corner(DR), 
                            color=GREEN, stroke_width=8
                        ))
            
            # Horizontal borders (check vertical neighbors)
            for r in range(3):
                for c in range(4):
                    idx1 = r * 4 + c
                    idx2 = (r + 1) * 4 + c
                    s1 = squares[idx1]
                    s2 = squares[idx2]
                    if s1.get_fill_color() != s2.get_fill_color():
                        count += 1
                        lines.add(Line(
                            s1.get_corner(DL), s1.get_corner(DR), 
                            color=GREEN, stroke_width=8
                        ))
            return count, lines

        # 3. Dynamic UI elements
        # Formula at the top
        formula = MathTex(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]").to_edge(UP)
        self.add(formula)

        # Counter display
        count_val, border_lines = get_adjacencies_and_lines()
        
        counter_label = Text("Border Count:", font_size=30).to_edge(RIGHT, buff=1.5).shift(UP)
        # Using DecimalNumber to avoid potential Integer issues
        counter_num = DecimalNumber(count_val, num_decimal_places=0, color=GREEN).scale(1.5).next_to(counter_label, DOWN)
        
        # Redraw borders and update counter every frame
        borders_group = always_redraw(lambda: get_adjacencies_and_lines()[1])
        
        def update_number(num_obj):
            val, _ = get_adjacencies_and_lines()
            num_obj.set_value(val)
            
        counter_num.add_updater(update_number)
        
        self.add(counter_label, counter_num, borders_group)

        # 4. Animation: Convert to Checkerboard
        # Pattern: (row + col) % 2 == 0 -> RED, else BLUE
        self.wait(1)
        
        # We process squares that need changing
        for i in range(16):
            r, c = i // 4, i % 4
            target_color = RED if (r + c) % 2 == 0 else BLUE
            
            if squares[i].get_fill_color() != target_color:
                self.play(
                    squares[i].animate.set_fill(target_color),
                    run_time=0.3
                )

        # 5. Conclusion
        conclusion = Text("Checkerboard maximizes interaction", font_size=24, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.play(Write(conclusion))
        self.wait(2)