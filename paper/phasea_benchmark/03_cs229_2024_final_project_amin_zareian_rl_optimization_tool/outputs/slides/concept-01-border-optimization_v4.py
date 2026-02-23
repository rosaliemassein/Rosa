from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # Create a 4x4 grid of Square objects
        sq_grid = []
        grid_group = VGroup()
        for r in range(4):
            row = []
            for c in range(4):
                # Initially color the left half red and the right half blue
                # Left half: columns 0 and 1; Right half: columns 2 and 3
                initial_color = RED if c < 2 else BLUE
                sq = Square(side_length=0.8, fill_color=initial_color, fill_opacity=1.0, stroke_width=2)
                # Arrange squares in space using a coordinate list instead of np.array
                sq.move_to([(c - 1.5) * 0.9, (1.5 - r) * 0.9, 0])
                row.append(sq)
                grid_group.add(sq)
            sq_grid.append(row)
        
        self.add(grid_group)

        # Formula at the top of the scene
        formula = MathTex(r"B = \sum_{i,j \in \text{Neighbors}} [P_i \neq P_j]").to_edge(UP)
        self.add(formula)

        # Counter for adjacency count (B)
        counter_label = Text("B = ", font_size=36).to_corner(DL).shift([2, 0.5, 0])
        # The count starts at 4 for the initial split between red and blue halves
        count_mob = MathTex("4").next_to(counter_label, RIGHT)
        self.add(counter_label, count_mob)

        # VGroup to hold the green border lines
        border_lines = VGroup()
        
        # Helper to generate border lines and count adjacencies based on current colors
        def get_current_border_data():
            lines = VGroup()
            b_count = 0
            for row_idx in range(4):
                for col_idx in range(4):
                    # Horizontal adjacency (check the square to the immediate right)
                    if col_idx < 3:
                        if sq_grid[row_idx][col_idx].get_fill_color() != sq_grid[row_idx][col_idx+1].get_fill_color():
                            # Draw a vertical green line at the contact edge
                            p1 = sq_grid[row_idx][col_idx].get_corner([1, 1, 0]) # Upper Right
                            p2 = sq_grid[row_idx][col_idx].get_corner([1, -1, 0]) # Lower Right
                            lines.add(Line(p1, p2, color=GREEN, stroke_width=8))
                            b_count += 1
                    # Vertical adjacency (check the square immediately below)
                    if row_idx < 3:
                        if sq_grid[row_idx][col_idx].get_fill_color() != sq_grid[row_idx+1][col_idx].get_fill_color():
                            # Draw a horizontal green line at the contact edge
                            p1 = sq_grid[row_idx][col_idx].get_corner([1, -1, 0]) # Lower Right
                            p2 = sq_grid[row_idx][col_idx].get_corner([-1, -1, 0]) # Lower Left
                            lines.add(Line(p1, p2, color=GREEN, stroke_width=8))
                            b_count += 1
            return lines, b_count

        # Initialize the border lines based on starting colors
        init_lines, _ = get_current_border_data()
        border_lines.add(*init_lines)
        self.add(border_lines)

        # Transition squares one by one to form a checkerboard pattern
        for row_idx in range(4):
            for col_idx in range(4):
                # Target color for the checkerboard (alternating pattern)
                target_color = RED if (row_idx + col_idx) % 2 == 0 else BLUE
                
                # If the square is not already the target color, flip it
                if sq_grid[row_idx][col_idx].get_fill_color() != target_color:
                    # Animate the color transition
                    self.play(
                        sq_grid[row_idx][col_idx].animate.set_fill(target_color),
                        run_time=0.25
                    )
                    
                    # Recalculate and update the green border lines and counter value
                    new_lines, new_count = get_current_border_data()
                    border_lines.become(new_lines)
                    
                    # Update the adjacency count display
                    new_count_mob = MathTex(str(new_count)).next_to(counter_label, RIGHT)
                    count_mob.become(new_count_mob)

        self.wait(2)