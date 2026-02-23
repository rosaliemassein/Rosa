from manim import *

class DominantZoneMechanism(Scene):
    def construct(self):
        # Explicit hex color definitions to ensure compatibility across Manim versions
        # BLUE_C equivalent
        C_NORMAL_BLUE = "#58C4DD"
        # BLUE_E equivalent
        C_DEEP_BLUE = "#236B8E"
        # BLUE_A equivalent
        C_LIGHT_BLUE = "#C7E9F1"
        
        # 1. Setup the Central AHU and surrounding Zones
        # AHU is at the top
        ahu = Rectangle(color=C_NORMAL_BLUE, width=2.5, height=1.2, fill_opacity=0.8)
        ahu_label = Text("AHU", font_size=24).move_to(ahu)
        ahu_group = VGroup(ahu, ahu_label).to_edge(UP, buff=1)

        # Five smaller rectangles for Zones at the bottom
        # Each zone is a VGroup of a Rectangle and its label
        zones = VGroup(*[
            VGroup(
                Rectangle(color=GREEN, width=1.5, height=1, fill_opacity=0.4),
                Text(f"Zone {i+1}", font_size=16).shift(DOWN * 0.7)
            ) for i in range(5)
        ])
        zones.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=1.5)

        self.add(ahu_group, zones)

        # 2. Animate heat gradient (orange) growing in two zones (indices 1 and 3)
        dominant_indices = [1, 3]
        heat_animations = [
            zones[i][0].animate.set_color(ORANGE).set_fill(ORANGE, opacity=0.8)
            for i in dominant_indices
        ]
        
        self.play(*heat_animations, run_time=2)

        # 3. Show dashed arrows moving from the orange zones to the AHU labeled 'Cooling Request'
        request_arrows = VGroup(*[
            DashedLine(
                zones[i].get_top(), 
                ahu.get_bottom(), 
                color=ORANGE, 
                dash_length=0.1
            ).add_tip()
            for i in dominant_indices
        ])
        request_label = Text("Cooling Request", font_size=20, color=ORANGE).next_to(request_arrows, RIGHT, buff=0.5)

        self.play(Create(request_arrows), Write(request_label), run_time=2)
        self.wait(0.5)

        # 4. As arrows hit AHU, change color from normal blue to deep blue
        self.play(
            ahu.animate.set_color(C_DEEP_BLUE).set_fill(C_DEEP_BLUE, opacity=1),
            FadeOut(request_label),
            run_time=1
        )

        # 5. Show deep blue 'Supply Air' arrows flowing back to ALL zones
        supply_arrows = VGroup(*[
            Arrow(
                ahu.get_bottom(), 
                zones[i].get_top(), 
                color=C_DEEP_BLUE, 
                buff=0.1, 
                stroke_width=4
            )
            for i in range(5)
        ])
        supply_label = Text("Supply Air", font_size=20, color=C_DEEP_BLUE).next_to(supply_arrows, LEFT, buff=0.5)

        self.play(Create(supply_arrows), Write(supply_label), run_time=2)

        # 6. The non-dominant green zones should then turn a 'chilled' white-blue color to signify overcooling
        overcool_animations = [
            zones[i][0].animate.set_color(C_LIGHT_BLUE).set_fill(C_LIGHT_BLUE, opacity=0.4)
            for i in range(5) if i not in dominant_indices
        ]
        
        self.play(*overcool_animations, run_time=1.5)
        self.wait(2)