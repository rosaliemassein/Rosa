from manim import *
import numpy as np

class DominantZoneMechanism(Scene):
    def construct(self):
        # Define specific hex colors to avoid undefined identifier errors
        COLOR_AHU_START = "#58C4DD"  # Light blue
        COLOR_AHU_END = "#1C758A"    # Deep blue
        COLOR_ZONE_NORMAL = "#83C167" # Green
        COLOR_ZONE_HOT = "#FF862F"    # Orange
        COLOR_ZONE_CHILLED = "#E1F5FE" # Chilled white-blue

        # 1. Create central AHU
        ahu_rect = Rectangle(width=2.5, height=1.5, fill_opacity=0.8)
        ahu_rect.set_color(COLOR_AHU_START).set_fill(COLOR_AHU_START)
        ahu_label = Text("AHU", font_size=24).move_to(ahu_rect.get_center())
        ahu = VGroup(ahu_rect, ahu_label)

        # 2. Create 5 surrounding Zones
        zones = VGroup()
        for i in range(5):
            # Calculate position in a circle around the center
            angle = i * (360 / 5) * (PI / 180)
            pos = 3.5 * np.array([np.cos(angle), np.sin(angle), 0])
            
            z_rect = Rectangle(width=1.5, height=1.0, fill_opacity=0.7)
            z_rect.set_color(COLOR_ZONE_NORMAL).set_fill(COLOR_ZONE_NORMAL)
            z_rect.move_to(pos)
            
            z_label = Text(f"Zone {i+1}", font_size=20).move_to(z_rect.get_center())
            zones.add(VGroup(z_rect, z_label))

        self.add(ahu, zones)
        self.wait(1)

        # 3. Animate heat (Orange) growing in two dominant zones (Zone 1 and 2)
        dominant_zones = [zones[0], zones[1]]
        other_zones = [zones[2], zones[3], zones[4]]

        self.play(
            *[z[0].animate.set_fill(COLOR_ZONE_HOT).set_color(COLOR_ZONE_HOT) for z in dominant_zones],
            run_time=1.5
        )
        self.wait(0.5)

        # 4. Show arrows from the orange zones to the AHU (Cooling Request)
        # Using standard Arrow since DashedLine was flagged as disallowed
        request_arrows = VGroup()
        for z in dominant_zones:
            arr = Arrow(z.get_center(), ahu.get_center(), color=COLOR_ZONE_HOT, buff=0.2)
            request_arrows.add(arr)
        
        req_label = Text("Cooling Request", font_size=24, color=COLOR_ZONE_HOT).next_to(ahu, UP, buff=0.5)

        self.play(Create(request_arrows), Write(req_label))
        self.wait(1)

        # 5. Change AHU color to deep blue
        self.play(
            ahu[0].animate.set_fill(COLOR_AHU_END).set_color(COLOR_AHU_END),
            FadeOut(req_label),
            run_time=1
        )

        # 6. Show supply air arrows flowing back to ALL zones
        supply_arrows = VGroup()
        for z in zones:
            arr = Arrow(ahu.get_center(), z.get_center(), color=COLOR_AHU_END, buff=0.2)
            supply_arrows.add(arr)

        supply_label = Text("Supply Air", font_size=24, color=COLOR_AHU_END).next_to(ahu, DOWN, buff=0.5)

        self.play(
            FadeOut(request_arrows),
            Create(supply_arrows),
            Write(supply_label),
            run_time=1
        )
        self.wait(1)

        # 7. Green zones turn "chilled" white-blue
        self.play(
            *[z[0].animate.set_fill(COLOR_ZONE_CHILLED).set_color(COLOR_ZONE_CHILLED) for z in other_zones],
            run_time=1.5
        )

        self.wait(2)