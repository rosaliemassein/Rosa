from manim import *

class DominantZoneMechanism(Scene):
    def construct(self):
        # Color definitions using hex codes to avoid undefined identifier errors
        C_LIGHT_BLUE = "#87CEEB"
        C_DARK_BLUE = "#00008B"
        C_CHILLED = "#F0F8FF"
        C_ORANGE = "#FFA500"
        C_GREEN = "#228B22"

        # Create central AHU and surrounding zones
        ahu = Rectangle(height=2, width=3, fill_color=C_LIGHT_BLUE, fill_opacity=1).move_to(ORIGIN)
        ahu_label = Text("AHU", font_size=24).move_to(ahu.get_center())

        zone_positions = [
            UP * 2.5 + LEFT * 3.5,
            UP * 2.5 + RIGHT * 3.5,
            DOWN * 2.5 + LEFT * 3.5,
            DOWN * 2.5 + RIGHT * 3.5,
            RIGHT * 5
        ]

        zones = VGroup(*[
            Rectangle(height=1.2, width=2.2, fill_color=C_GREEN, fill_opacity=1).move_to(pos)
            for pos in zone_positions
        ])
        
        zone_labels = VGroup(*[
            Text(f"Zone {i+1}", font_size=20).move_to(zones[i].get_center())
            for i in range(5)
        ])

        self.add(ahu, ahu_label, zones, zone_labels)
        self.wait(1)

        # 1. Heat gradient (orange) growing in two dominant zones
        dominant_indices = [0, 1]
        self.play(
            *[zones[i].animate.set_fill(C_ORANGE) for i in dominant_indices],
            run_time=1.5
        )
        self.wait(0.5)

        # 2. Show arrows from orange zones to AHU labeled 'Cooling Request'
        # Using Line + add_tip since DashedLine is disallowed in this subset
        request_arrows = VGroup(*[
            Line(zones[i].get_center(), ahu.get_center(), color=C_ORANGE, stroke_width=4).add_tip()
            for i in dominant_indices
        ])
        request_text = Text("Cooling Request", font_size=24, color=C_ORANGE).next_to(ahu, UP, buff=0.5)

        self.play(Create(request_arrows), Write(request_text))
        self.wait(1)

        # 3. AHU color changes to deep blue
        self.play(
            ahu.animate.set_fill(C_DARK_BLUE),
            FadeOut(request_text),
            run_time=1
        )

        # 4. Show supply air arrows flowing back to ALL zones
        supply_arrows = VGroup(*[
            Line(ahu.get_center(), zones[i].get_center(), color=C_DARK_BLUE, stroke_width=5).add_tip()
            for i in range(5)
        ])
        supply_text = Text("Supply Air (Colder)", font_size=24, color=C_DARK_BLUE).next_to(ahu, DOWN, buff=0.5)

        self.play(Create(supply_arrows), Write(supply_text))
        self.wait(1)

        # 5. Non-dominant zones turn a chilled white-blue color
        other_indices = [2, 3, 4]
        self.play(
            *[zones[i].animate.set_fill(C_CHILLED) for i in other_indices],
            *[zones[i].animate.set_fill(C_DARK_BLUE) for i in dominant_indices],
            run_time=1.5
        )

        self.wait(2)

        # Fade out elements
        self.play(
            FadeOut(ahu), 
            FadeOut(ahu_label), 
            FadeOut(zones), 
            FadeOut(zone_labels), 
            FadeOut(request_arrows), 
            FadeOut(supply_arrows), 
            FadeOut(supply_text)
        )