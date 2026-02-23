from manim import *

class AdaptiveVsStaticSelection(Scene):
    def construct(self):
        # Split-screen setup
        left_screen = Rectangle(width=6, height=4, color=BLUE)
        right_screen = Rectangle(width=6, height=4, color=YELLOW)

        floorplan_left = VGroup()
        floorplan_right = VGroup()

        # Initialize some example zones
        zone_1_left = Circle(radius=0.5, color=RED)
        zone_2_left = Circle(radius=0.5, color=BLUE)
        zone_3_left = Square(side_length=1, color=GREEN)

        zone_1_right = Circle(radius=0.5, color=RED)
        zone_2_right = Circle(radius=0.5, color=BLUE)
        zone_3_right = Square(side_length=1, color=GREEN)

        # Arrange zones
        for i in range(3):
            zone_1_left.next_to(floorplan_left, RIGHT)
            zone_2_left.next_to(zone_1_left, RIGHT)
            zone_3_left.next_to(zone_2_left, RIGHT)

            zone_1_right.next_to(floorplan_right, RIGHT)
            zone_2_right.next_to(zone_1_right, RIGHT)
            zone_3_right.next_to(zone_2_right, RIGHT)

            floorplan_left.add(zone_1_left)
            floorplan_left.add(zone_2_left)
            floorplan_left.add(zone_3_left)

            floorplan_right.add(zone_1_right)
            floorplan_right.add(zone_2_right)
            floorplan_right.add(zone_3_right)

        # Timeline
        timeline = Line(ORIGIN, RIGHT * 6)
        timeline.scale(0.5)
        timeline.shift(DOWN)

        # Missed Requests graph
        missed_requests_left = Line(ORIGIN, RIGHT * 6)
        missed_requests_right = Line(ORIGIN, RIGHT * 6)

        # Overlay for clarity
        guide_line = Circle(radius=0.1, color=WHITE).next_to(timeline, DOWN)

        # Animation setup
        missed_requests_left.shift(UP * 2)
        missed_requests_right.shift(DOWN * 1.5)

        # Initial setup
        self.add(left_screen, right_screen)
        self.add(floorplan_left)
        self.add(timeline)
        self.add(missed_requests_left, missed_requests_right)

        # Initial state
        self.play(Create(floorplan_left), Create(timeline), Write(missed_requests_left[0]), FadeIn(missed_requests_right[0]))
        self.wait(2)

        # Static benchmark
        missed_requests_left[1].set_color(BLUE)
        self.play(Transform(missed_requests_left, missed_requests_right))
        self.wait(1)

        # Adaptive ML
        self.play(Transform(missed_requests_left, missed_requests_right[0]))
        self.wait(1)

        # More zones highlighted
        zone_4_left = Circle(radius=0.5, color=PURPLE)
        zone_5_left = Square(side_length=1, color=YELLOW)

        zone_4_right = Circle(radius=0.5, color=PURPLE)
        zone_5_right = Square(side_length=1, color=YELLOW)

        floorplan_left.add(zone_4_left)
        floorplan_left.add(zone_5_left)

        floorplan_right.add(zone_4_right)
        floorplan_right.add(zone_5_right)

        self.play(Create(zone_4_left), Create(zone_5_left))
        self.wait(1)

        # Missed Requests show improvement
        missed_requests_right[1].set_color(BLUE)
        self.play(Transform(missed_requests_left, missed_requests_right))
        self.wait(1)

        # Final state
        zone_4_left.move_to(DOWN * 0.5)
        zone_5_left.move_to(DOWN * 1.5)

        self.play(Transform(zone_4_left, zone_4_right))
        self.wait(1)
        self.play(Transform(zone_5_left, zone_5_right))

        # Final note
        final_text = Text("Demonstrate the superiority of adaptive ML over static ASHRAE guidelines.").scale(0.8).to_edge(DOWN)
        self.play(Write(final_text))
        self.wait()