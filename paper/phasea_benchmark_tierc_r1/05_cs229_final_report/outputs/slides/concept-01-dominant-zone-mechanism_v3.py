from manim import *

class DominantZoneMechanism(Scene):
    def construct(self):
        # Hex color definitions to ensure compatibility and avoid undefined identifier errors
        ORANGE_HEX = "#FFA500"
        DARK_BLUE_HEX = "#00008B"
        LIGHT_BLUE_HEX = "#ADD8E6"
        GREEN_HEX = "#008000"
        CHILLED_HEX = "#F0F8FF" # AliceBlue
        
        # 1. Create the AHU and zones
        ahu = Rectangle(width=2.5, height=1.8, color=WHITE)
        ahu.set_fill(LIGHT_BLUE_HEX, opacity=0.3)
        ahu_label = Text("AHU", font_size=28).move_to(ahu.get_center())
        ahu_group = VGroup(ahu, ahu_label).to_edge(UP, buff=0.5)

        # Create 5 zones
        zones = VGroup(*[
            Rectangle(width=1.8, height=1.2, color=GREEN_HEX)
            for _ in range(5)
        ])
        
        # Position zones around the center/bottom area
        positions = [
            4 * LEFT + 1 * DOWN,
            2 * LEFT + 1 * DOWN,
            0 * LEFT + 1 * DOWN,
            2 * RIGHT + 1 * DOWN,
            4 * RIGHT + 1 * DOWN
        ]
        
        for i, pos in enumerate(positions):
            zones[i].move_to(pos)
            zones[i].set_fill(GREEN_HEX, opacity=0.2)
        
        zone_labels = VGroup(*[
            Text(f"Zone {i+1}", font_size=16).next_to(zones[i], DOWN, buff=0.1)
            for i in range(5)
        ])

        self.play(FadeIn(ahu_group), FadeIn(zones), FadeIn(zone_labels))
        self.wait(1)

        # 2. Animate a heat gradient (orange) growing in two dominant zones
        # We'll use zones 0 and 1 as the "dominant" ones
        self.play(
            zones[0].animate.set_fill(ORANGE_HEX, opacity=0.8).set_color(ORANGE_HEX),
            zones[1].animate.set_fill(ORANGE_HEX, opacity=0.8).set_color(ORANGE_HEX),
            run_time=1.5
        )
        self.wait(0.5)

        # 3. Dashed arrows from orange zones to AHU labeled 'Cooling Request'
        req_arrow1 = DashedLine(zones[0].get_top(), ahu.get_bottom(), color=ORANGE_HEX).add_tip()
        req_arrow2 = DashedLine(zones[1].get_top(), ahu.get_bottom(), color=ORANGE_HEX).add_tip()
        req_label = Text("Cooling Request", font_size=20, color=ORANGE_HEX).move_to(LEFT * 3 + UP * 0.5)

        self.play(Create(req_arrow1), Create(req_arrow2), Write(req_label))
        self.wait(0.5)

        # 4. As arrows hit the AHU, change its color to deep blue
        self.play(
            ahu.animate.set_fill(DARK_BLUE_HEX, opacity=0.9).set_color(DARK_BLUE_HEX),
            ahu_label.animate.set_color(WHITE),
            run_time=1
        )
        self.wait(0.5)

        # 5. Show deep blue 'Supply Air' arrows flowing back to ALL zones
        supply_arrows = VGroup(*[
            DashedLine(ahu.get_bottom(), zones[i].get_top(), color=DARK_BLUE_HEX).add_tip()
            for i in range(5)
        ])
        supply_label = Text("Supply Air (Decreased Temp)", font_size=20, color=DARK_BLUE_HEX).next_to(ahu, RIGHT, buff=0.5)

        self.play(Create(supply_arrows), Write(supply_label))
        self.wait(1)

        # 6. Green zones turn 'chilled' white-blue color to signify overcooling
        # And the orange zones satisfy their demand (turning back to a cool color)
        self.play(
            zones[2].animate.set_fill(CHILLED_HEX, opacity=0.8).set_color(CHILLED_HEX),
            zones[3].animate.set_fill(CHILLED_HEX, opacity=0.8).set_color(CHILLED_HEX),
            zones[4].animate.set_fill(CHILLED_HEX, opacity=0.8).set_color(CHILLED_HEX),
            zones[0].animate.set_fill(LIGHT_BLUE_HEX, opacity=0.8).set_color(LIGHT_BLUE_HEX),
            zones[1].animate.set_fill(LIGHT_BLUE_HEX, opacity=0.8).set_color(LIGHT_BLUE_HEX),
            run_time=2
        )

        # 7. Conclusion text
        conclusion = Text(
            "Overcooling occurs building-wide to satisfy the most demanding zones.",
            font_size=22
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(conclusion))
        self.wait(3)