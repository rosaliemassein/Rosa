from manim import *
import math

class DominantZoneMechanism(Scene):
    def construct(self):
        # Using hex codes to avoid undefined color constant errors
        COLOR_AHU_LIGHT = "#58C4DD"  # Light Blue
        COLOR_AHU_DEEP = "#236B8E"   # Deep Blue
        COLOR_ZONE_NORMAL = "#83C167" # Green
        COLOR_ZONE_HOT = "#FF862F"    # Orange
        COLOR_ZONE_CHILLED = "#C7E9F1" # White-Blue
        COLOR_SUPPLY = "#236B8E"      # Deep Blue

        # 1. Create central AHU and surrounding Zones
        ahu = Rectangle(width=3, height=1.5, color=COLOR_AHU_LIGHT).set_fill(COLOR_AHU_LIGHT, opacity=0.5)
        ahu_label = Text("AHU", font_size=24).move_to(ahu.get_center())
        ahu_group = VGroup(ahu, ahu_label).move_to(ORIGIN)

        zones = VGroup()
        zone_labels = VGroup()
        for i in range(5):
            angle = i * 2 * math.pi / 5
            # Position zones in a circle around the AHU
            z = Rectangle(width=1.5, height=0.8, color=COLOR_ZONE_NORMAL).set_fill(COLOR_ZONE_NORMAL, opacity=0.5)
            pos = [4.0 * math.cos(angle), 2.5 * math.sin(angle), 0]
            z.move_to(pos)
            zones.add(z)
            
            label = Text(f"Zone {i+1}", font_size=18).move_to(pos)
            zone_labels.add(label)

        self.play(Create(ahu_group), Create(zones), Create(zone_labels))
        self.wait(1)

        # 2. Animate heat gradient (orange) growing in two zones
        hot_indices = [1, 3]
        hot_zones_group = VGroup(*[zones[i] for i in hot_indices])
        
        self.play(
            *[z.animate.set_fill(COLOR_ZONE_HOT, opacity=0.8).set_color(COLOR_ZONE_HOT) for z in hot_zones_group]
        )
        self.wait(1)

        # 3. Cooling requests (arrows from hot zones to AHU)
        # Using standard Arrow to ensure compatibility
        requests = VGroup()
        for i in hot_indices:
            req = Arrow(zones[i].get_center(), ahu.get_center(), color=COLOR_ZONE_HOT, buff=0.8)
            requests.add(req)
        
        req_text = Text("Cooling Request", font_size=20, color=COLOR_ZONE_HOT).next_to(ahu, UP, buff=0.5)
        
        self.play(Create(requests), Write(req_text))
        self.wait(1)

        # 4. AHU color changes to deep blue when requests arrive
        self.play(
            ahu.animate.set_fill(COLOR_AHU_DEEP, opacity=1).set_color(COLOR_AHU_DEEP),
            FadeOut(requests),
            FadeOut(req_text)
        )
        self.wait(0.5)

        # 5. Supply Air back to all zones
        supply_arrows = VGroup()
        for z in zones:
            sa = Arrow(ahu.get_center(), z.get_center(), color=COLOR_SUPPLY, buff=0.8)
            supply_arrows.add(sa)
        
        supply_text = Text("Supply Air", font_size=20, color=COLOR_SUPPLY).next_to(ahu, DOWN, buff=0.5)
        
        self.play(Create(supply_arrows), Write(supply_text))
        self.wait(1)

        # 6. Green (normal) zones turn chilled white-blue to signify overcooling
        cool_indices = [0, 2, 4]
        cool_zones_group = VGroup(*[zones[i] for i in cool_indices])
        
        self.play(
            *[z.animate.set_fill(COLOR_ZONE_CHILLED, opacity=0.8).set_color(COLOR_ZONE_CHILLED) for z in cool_zones_group],
            FadeOut(supply_arrows),
            FadeOut(supply_text)
        )
        self.wait(2)