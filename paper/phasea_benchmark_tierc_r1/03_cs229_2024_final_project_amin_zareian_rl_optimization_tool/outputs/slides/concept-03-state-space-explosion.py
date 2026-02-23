from manim import *

class StateSpaceExplosion(Scene):
    def construct(self):
        # Axes setup
        axes = Axes(
            x_range=[2, 6],
            y_range=[1e-5, 10**9], 
            x_label="Matrix Size",
            y_label="Possible States (log scale)",
            axis_config={"stroke_width": 2},
            y_axis_label=Tex(r"log(y)", color=YELLOW)
        ).to_edge(UL)

        # Initial 2x2 table
        initial_table = VGroup(
            *[
                Text(row, color=YELLOW).next_to(axes, DOWN, buff=0.2) for row in [
                    "R,B",
                    "B,R"
                ]
            ]
        ).scale(0.5).next_to(axes, DOWN)

        # Draw the initial table
        self.play(Create(axes), Write(initial_table))

        # Animate increasing grid size
        for i, n in enumerate([2, 3, 4, 5]):
            # Create new rows
            new_rows = VGroup(
                *[
                    Text(f"{row}", color=YELLOW).next_to(axes, DOWN, buff=0.2) for row in [
                        *[
                            "R,B", "B,R"
                        ] * n
                    ]
                ]
            )
            
            # Create dashed lines for transitions
            dashed_line = DashedLine(left=axes.x_min - 1, right=axes.y_max + 2).next_to(axes, DOWN, buff=0.1)
            
            # Animate insertions and transitions
            for row in new_rows:
                self.play(Transform(dashed_line.copy(), dashed_line), Write(row))
            
            # Add a pause to create the illusion of scrolling
            self.wait(0.25)

        # Final animation: solid blur of color and growing curve
        self.play(
            Transform(initial_table, VGroup(*[Text("R,B", color=YELLOW) for _ in range(25)]).scale(0.5).next_to(axes, DOWN)),
            Transform(dashed_line.copy(), dashed_line.resize_to(5*axes.get_height())),
            FadeOut(VGroup(*[Text("R,B", color=YELLOW) for _ in range(16)]).scale(0.5).next_to(axes, DOWN)),
            Write(Arrow(axes.x_min - 1.5, axes.y_max + 2.5)).set_color(GREEN).scale(0.5)
        )