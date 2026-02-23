from manim import *

class DominantZoneMechanism(Scene):
    def construct(self):
        # 1. Create the AHU (Central Unit)
        # Using standard colors and basic Rectangle/Text
        ahu_rect = Rectangle(height=2, width=3).set_fill(BLUE, opacity=0.3)
        ahu_label = Text("AHU", font_size=24)
        ahu = VGroup(ahu_rect, ahu_label)

        # 2. Create five smaller surrounding zones
        # Define explicit positions to ensure they surround the center
        zone_positions = [
            [-4, 2, 0],   # Top Left
            [4, 2, 0],    # Top Right
            [-4, -1, 0],  # Left
            [4, -1, 0],   # Right
            [0, -3, 0]    # Bottom
        ]
        
        zones = VGroup(*[
            Rectangle(height=1.2, width=1.8).set_fill(GREEN, opacity=0.5).move_to(pos)
            for pos in zone_positions
        ])
        
        self.add(ahu, zones)
        self.wait(1)

        # 3. Animate heat growth in two dominant zones
        # Changing Zone 0 and Zone 1 to Orange
        self.play(
            zones[0].animate.set_fill(ORANGE, opacity=0.8),
            zones[1].animate.set_fill(ORANGE, opacity=0.8),
            run_time=2
        )
        self.wait(1)

        # 4. Cooling Request arrows (using standard Arrow as DashedLine is restricted)
        req_arrow1 = Arrow(zones[0].get_bottom(), ahu_rect.get_left(), color=ORANGE, buff=0.1)
        req_arrow2 = Arrow(zones[1].get_bottom(), ahu_rect.get_right(), color=ORANGE, buff=0.1)
        req_label = Text("Cooling Request", font_size=20, color=ORANGE).next_to(ahu_rect, UP)

        self.play(
            Create(req_arrow1),
            Create(req_arrow2),
            Write(req_label)
        )
        self.wait(1)

        # 5. AHU response: Color shifts to a deeper blue (higher opacity)
        self.play(
            ahu_rect.animate.set_fill(BLUE, opacity=1.0),
            req_label.animate.set_color(BLUE)
        )
        self.wait(1)

        # 6. Supply Air arrows flowing back to ALL zones
        supply_arrows = VGroup(*[
            Arrow(ahu_rect.get_center(), zones[i].get_center(), color=BLUE, buff=0.7)
            for i in range(5)
        ])
        supply_label = Text("Supply Air", font_size=20, color=BLUE).next_to(ahu_rect, DOWN)

        self.play(
            Create(supply_arrows),
            Write(supply_label)
        )
        self.wait(1)

        # 7. Green zones turn "chilled" white-blue (signifying overcooling)
        # We use WHITE with a blue stroke as a proxy for chilled white-blue
        self.play(
            zones[2].animate.set_fill(WHITE, opacity=0.8).set_stroke(BLUE),
            zones[3].animate.set_fill(WHITE, opacity=0.8).set_stroke(BLUE),
            zones[4].animate.set_fill(WHITE, opacity=0.8).set_stroke(BLUE),
            run_time=2
        )
        
        self.wait(2)