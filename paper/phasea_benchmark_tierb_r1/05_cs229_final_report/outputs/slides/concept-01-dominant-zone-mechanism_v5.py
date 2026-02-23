from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
        # 1. Create the AHU (Air Handling Unit)
        ahu = Rectangle(width=3, height=2, color=BLUE, fill_color=BLUE, fill_opacity=0.8)
        ahu_label = Text("AHU", color=WHITE).scale(0.8)
        ahu_group = VGroup(ahu, ahu_label)
        
        # 2. Create 5 smaller rectangles (Zones) surrounding the AHU
        zones = VGroup(*[
            Rectangle(width=1.5, height=1, color=GREEN, fill_color=GREEN, fill_opacity=0.8)
            for _ in range(5)
        ])
        
        # Position zones in a circle around the AHU using numpy
        for i, zone in enumerate(zones):
            angle = i * (360 / 5) * DEGREES
            # Standard radius for placement
            zone.move_to(3.5 * np.array([np.cos(angle), np.sin(angle), 0]))
        
        self.play(Create(ahu_group))
        self.play(Create(zones))
        self.wait(1)

        # 3. Animate heat (orange) growing in two zones
        # Indices 0 and 1 are chosen as dominant zones
        self.play(
            zones[0].animate.set_fill(ORANGE).set_stroke(ORANGE),
            zones[1].animate.set_fill(ORANGE).set_stroke(ORANGE),
            run_time=2
        )
        self.wait(1)

        # 4. Show arrows moving from the orange zones to the AHU (Cooling Request)
        # Using standard Arrow since DashedLine is disallowed
        req_arrow1 = Arrow(zones[0].get_center(), ahu.get_center(), color=ORANGE, buff=0.8)
        req_arrow2 = Arrow(zones[1].get_center(), ahu.get_center(), color=ORANGE, buff=0.8)
        
        req_label = Text("Cooling Request", color=ORANGE).scale(0.5).to_edge(UP, buff=0.5)
        
        self.play(Create(req_arrow1), Create(req_arrow2), Write(req_label))
        self.wait(1)

        # 5. Change AHU color to a deeper blue to show response
        dark_blue_hex = "#00008B"
        self.play(
            ahu.animate.set_fill(dark_blue_hex).set_stroke(dark_blue_hex),
            FadeOut(req_arrow1),
            FadeOut(req_arrow2),
            FadeOut(req_label),
            run_time=1
        )

        # 6. Show supply air arrows flowing back to ALL zones
        supply_arrows = VGroup(*[
            Arrow(ahu.get_center(), zone.get_center(), color=dark_blue_hex, buff=0.8)
            for zone in zones
        ])
        
        supply_label = Text("Supply Air (Colder)", color=dark_blue_hex).scale(0.5).to_edge(UP, buff=0.5)
        
        self.play(Create(supply_arrows), Write(supply_label))
        self.wait(1)

        # 7. Green zones turn a chilled white-blue color (overcooling)
        chilled_blue = "#E1F5FE"
        self.play(
            zones[2].animate.set_fill(chilled_blue).set_stroke(chilled_blue),
            zones[3].animate.set_fill(chilled_blue).set_stroke(chilled_blue),
            zones[4].animate.set_fill(chilled_blue).set_stroke(chilled_blue),
            run_time=2
        )
        
        # 8. Add goal text narration
        goal_text = Text(
            "Understand the physical relationship between individual zone requests\nand building-wide HVAC behavior.",
            color=WHITE
        ).scale(0.5).to_edge(DOWN, buff=0.5)
        
        self.play(Write(goal_text))
        self.wait(3)