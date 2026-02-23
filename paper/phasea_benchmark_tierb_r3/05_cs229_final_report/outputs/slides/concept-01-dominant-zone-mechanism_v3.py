from manim import *

class DominantZoneMechanism(Scene):
    def construct(self):
        # Using hex color codes to avoid undefined constant issues in restricted environments
        COLOR_BLUE_LIGHT = "#58C4DD"
        COLOR_BLUE_DARK = "#1C758A"
        COLOR_GREEN = "#83C167"
        COLOR_ORANGE = "#FF8C00"
        COLOR_CHILLED = "#C5E3EC"
        COLOR_WHITE = "#FFFFFF"

        # 1. Setup the AHU (Air Handling Unit)
        ahu_box = Rectangle(height=1.5, width=3.0, fill_color=COLOR_BLUE_LIGHT, fill_opacity=0.8)
        ahu_label = Text("AHU").scale(0.7).move_to(ahu_box.get_center())
        ahu = VGroup(ahu_box, ahu_label).shift(DOWN * 2)

        # 2. Setup 5 Zones
        zones = VGroup(*[
            Rectangle(height=1.0, width=1.5, fill_color=COLOR_GREEN, fill_opacity=0.8) 
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.4).to_edge(UP, buff=1)
        
        # Add labels for zones
        labels = VGroup(*[
            Text(str(i+1)).scale(0.4).move_to(zones[i].get_center())
            for i in range(5)
        ])

        self.add(ahu, zones, labels)
        self.wait(1)

        # 3. Initial Narration
        narr_text = Text("A few dominant zones drive the building's energy load.").scale(0.5).to_edge(DOWN)
        self.play(Write(narr_text))
        self.wait(1)

        # 4. Heat gradient: Two zones (1 and 3) become hot (orange)
        hot_indices = [1, 3]
        self.play(
            *[zones[i].animate.set_fill(COLOR_ORANGE) for i in hot_indices],
            run_time=2
        )
        self.wait(0.5)

        # 5. Cooling requests (Arrows from orange zones to AHU)
        # Using standard Arrow as DashedLine is restricted
        req_arrows = VGroup(*[
            Arrow(zones[i].get_bottom(), ahu_box.get_top(), color=COLOR_ORANGE, buff=0.1)
            for i in hot_indices
        ])
        req_label = Text("Cooling Request").scale(0.4).set_color(COLOR_ORANGE).next_to(req_arrows, RIGHT, buff=0.2)
        
        self.play(Create(req_arrows), Write(req_label))
        self.wait(1)

        # 6. AHU responds: Color change from light blue to deep blue
        self.play(
            ahu_box.animate.set_fill(COLOR_BLUE_DARK),
            FadeOut(req_arrows),
            FadeOut(req_label),
            run_time=1
        )

        # 7. Supply air to ALL zones (Deep blue arrows)
        supply_arrows = VGroup(*[
            Arrow(ahu_box.get_top(), zones[i].get_bottom(), color=COLOR_BLUE_DARK, buff=0.1)
            for i in range(5)
        ])
        supply_label = Text("Supply Air (Colder)").scale(0.4).set_color(COLOR_BLUE_DARK).next_to(ahu_box, RIGHT)
        
        self.play(Create(supply_arrows), Write(supply_label))
        self.wait(1)

        # 8. Overcooling: The green zones turn white-blue
        green_indices = [0, 2, 4]
        self.play(
            *[zones[i].animate.set_fill(COLOR_CHILLED) for i in green_indices],
            run_time=1.5
        )
        self.wait(1)

        # 9. Conclusion
        conclusion_text = Text("Building-wide HVAC behavior: satisfying the few overcools the many.").scale(0.45).to_edge(DOWN)
        self.play(ReplacementTransform(narr_text, conclusion_text))
        self.wait(2)