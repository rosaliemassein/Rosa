from manim import *

class ConceptZoneMechanism(Scene):
    def construct(self):
        # Using hex codes for colors to ensure compatibility across different Manim versions
        C_BLUE = "#236B8E"
        C_DARK_BLUE = "#003366"
        C_LIGHT_BLUE = "#ADD8E6"
        C_GREEN = "#83C167"
        C_ORANGE = "#FF8C00"
        C_WHITE = "#FFFFFF"

        # 1. Create the AHU (Central Rectangle)
        ahu = Rectangle(width=3, height=2, color=C_BLUE, fill_color=C_BLUE, fill_opacity=0.3)
        ahu.shift(UP * 2)
        ahu_label = Text("AHU", font_size=24).move_to(ahu.get_center())
        ahu_group = VGroup(ahu, ahu_label)

        # 2. Create the Zones (Five smaller rectangles)
        zones = VGroup(*[
            Rectangle(width=1.5, height=1, color=C_GREEN, fill_color=C_GREEN, fill_opacity=0.3)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.5).shift(DOWN * 1.5)
        
        zone_labels = VGroup(*[
            Text(f"Zone {i+1}", font_size=18).move_to(zones[i].get_center())
            for i in range(5)
        ])

        self.add(ahu_group, zones, zone_labels)
        self.wait(1)

        # 3. Animate a heat gradient (orange) growing in two zones (Zone 2 and Zone 4)
        hot_indices = [1, 3]
        self.play(
            *[zones[i].animate.set_fill(C_ORANGE, opacity=0.8).set_color(C_ORANGE) for i in hot_indices],
            run_time=2
        )
        self.wait(0.5)

        # 4. Show dashed arrows moving from the orange zones to the AHU (Cooling Request)
        cooling_requests = VGroup(*[
            DashedLine(
                zones[i].get_top(), 
                ahu.get_bottom(), 
                color=C_ORANGE, 
                stroke_width=4
            ).add_tip()
            for i in hot_indices
        ])
        req_text = Text("Cooling Request", color=C_ORANGE, font_size=24).next_to(cooling_requests, RIGHT)

        self.play(Create(cooling_requests), Write(req_text), run_time=1.5)
        self.wait(1)

        # 5. Change the color of the AHU from light blue to deep blue
        self.play(
            ahu.animate.set_fill(C_DARK_BLUE, opacity=1).set_color(C_DARK_BLUE),
            FadeOut(req_text),
            run_time=1
        )
        self.wait(0.5)

        # 6. Show deep blue 'Supply Air' arrows flowing back to ALL zones
        supply_arrows = VGroup(*[
            DashedLine(
                ahu.get_bottom(), 
                zones[i].get_top(), 
                color=C_DARK_BLUE, 
                stroke_width=4
            ).add_tip()
            for i in range(5)
        ])
        supply_text = Text("Supply Air (Colder)", color=C_DARK_BLUE, font_size=24).next_to(supply_arrows, LEFT)

        self.play(Create(supply_arrows), Write(supply_text), run_time=1.5)
        self.wait(1)

        # 7. Green zones turn a 'chilled' white-blue color (overcooling)
        chilled_indices = [0, 2, 4]
        self.play(
            *[zones[i].animate.set_fill(C_LIGHT_BLUE, opacity=0.5).set_color(C_WHITE) for i in chilled_indices],
            FadeOut(supply_text),
            run_time=1.5
        )
        
        # Add labels to indicate overcooling
        overcooled_labels = VGroup(*[
            Text("Overcooled", font_size=14, color=C_BLUE).next_to(zones[i], DOWN, buff=0.1)
            for i in chilled_indices
        ])
        self.play(Write(overcooled_labels))
        
        self.wait(2)