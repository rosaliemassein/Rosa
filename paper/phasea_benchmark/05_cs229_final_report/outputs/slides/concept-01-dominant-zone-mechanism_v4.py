from manim import *

class Concept01DominantZoneMechanism(Scene):
    def construct(self):
        # 1. Setup: Central AHU and five smaller surrounding Zones
        # AHU: using Square and scaling since Rectangle is disallowed
        ahu_box = Square(side_length=1.0).scale([2.5, 1.5, 1]).set_color(BLUE)
        ahu_box.set_fill(BLUE, opacity=0.3)
        ahu_box.to_edge(RIGHT, buff=1.5)
        ahu_label = Text("AHU", font_size=32).move_to(ahu_box.get_center())

        # Zones: five smaller squares scaled to look like rectangles
        zones = VGroup()
        zone_labels = VGroup()
        for i in range(5):
            z = Square(side_length=1.0).scale([1.8, 0.8, 1]).set_color(GREEN)
            z.set_fill(GREEN, opacity=0.3)
            zones.add(z)
            lbl = Text(f"Zone {i+1}", font_size=20).move_to(z.get_center())
            zone_labels.add(lbl)
            
        zones.arrange(DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        for i in range(5):
            zone_labels[i].move_to(zones[i].get_center())

        self.play(
            Create(ahu_box), 
            Write(ahu_label), 
            Create(zones), 
            Write(zone_labels)
        )
        self.wait(1)

        # 2. Animate a heat gradient (orange) growing in two dominant zones
        # Using Hex for Orange as the identifier might be undefined
        HEX_ORANGE = "#FFA500"
        dominant_indices = [0, 1]
        self.play(
            *[zones[i].animate.set_fill(HEX_ORANGE, opacity=0.8).set_color(HEX_ORANGE) for i in dominant_indices],
            run_time=2
        )
        self.wait(0.5)

        # 3. Arrows 'Cooling Request' from orange zones to AHU
        # Using Line + Tip because DashedLine was undefined
        requests = VGroup()
        for i in dominant_indices:
            req_arrow = Line(
                zones[i].get_right(), 
                ahu_box.get_left(), 
                color=RED
            ).add_tip()
            requests.add(req_arrow)
        
        req_text = Text("Cooling Request", color=RED, font_size=24).next_to(ahu_box, UP, buff=0.5)
        
        self.play(Create(requests), Write(req_text))
        self.wait(1)

        # 4. AHU changes color to deep blue
        HEX_DEEP_BLUE = "#00008B"
        self.play(
            ahu_box.animate.set_fill(HEX_DEEP_BLUE, opacity=1.0).set_color(HEX_DEEP_BLUE),
            FadeOut(requests),
            FadeOut(req_text)
        )
        self.wait(0.5)

        # 5. Supply air arrows flowing back to ALL zones
        supply_arrows = VGroup()
        for i in range(5):
            sa_arrow = Line(
                ahu_box.get_left(), 
                zones[i].get_right(), 
                color=BLUE, 
                stroke_width=4
            ).add_tip()
            supply_arrows.add(sa_arrow)
        
        sa_text = Text("Supply Air", color=BLUE, font_size=24).next_to(ahu_box, UP, buff=0.5)
        
        self.play(Create(supply_arrows), Write(sa_text))
        self.wait(1)

        # 6. Green zones turn a 'chilled' white-blue color to signify overcooling
        HEX_CHILLED = "#E0FFFF"
        overcooled_indices = [2, 3, 4]
        
        self.play(
            *[zones[i].animate.set_fill(HEX_CHILLED, opacity=0.8).set_color(HEX_CHILLED) for i in overcooled_indices],
            run_time=2
        )
        self.wait(2)

        # Final cleanup
        self.play(
            *[FadeOut(m) for m in [ahu_box, ahu_label, zones, zone_labels, supply_arrows, sa_text]]
        )
        self.wait(1)