from manim import *

class Concept02OpponentAbstraction(Scene):
    def construct(self):
        # 1. Formula Display
        # Reference: S \in \mathbb{B}^{n \times n \times 3}
        formula = MathTex(r"S \in \mathbb{B}^{n \times n \times 3}").to_edge(UP)
        self.play(Write(formula))
        self.wait(0.5)

        # 2. 2-Player Board Representation
        # Layer 1: Me (Blue), Layer 2: Opponent (Red)
        me_layer = Square(color=BLUE, fill_opacity=0.6).scale(1.2)
        opp_layer = Square(color=RED, fill_opacity=0.6).scale(1.2).shift(RIGHT * 0.3 + UP * 0.3)
        
        me_label = Text("Me Channel", color=BLUE).scale(0.5).to_corner(DL, buff=1)
        opp_label_2p = Text("Opponent Channel", color=RED).scale(0.5).to_corner(UR, buff=1)
        
        self.play(
            Create(me_layer), 
            Write(me_label)
        )
        self.play(
            Create(opp_layer), 
            Write(opp_label_2p)
        )
        self.wait(1)

        # 3. 6-Player Board with 5 different opponent colors
        # Defining 5 manual red-ish colors to avoid "undefined identifier" errors like RED_A
        shades_of_red = ["#FF3333", "#CC0000", "#FF6666", "#990000", "#FF0000"]
        
        opponents_6p = VGroup()
        for i, shade in enumerate(shades_of_red):
            s = Square(color=shade, fill_opacity=0.6).scale(1.2).shift(RIGHT * (0.3 + i * 0.1) + UP * (0.3 + i * 0.1))
            opponents_6p.add(s)
            
        six_player_label = Text("5 Individual Opponents", color=RED).scale(0.5).to_edge(RIGHT).shift(UP * 2)

        self.play(
            ReplacementTransform(opp_layer, opponents_6p),
            ReplacementTransform(opp_label_2p, six_player_label)
        )
        self.wait(1)

        # 4. Animate the 5 opponent colors merging into a single 'Red' intensity
        # This unified layer represents the abstraction
        unified_opp_layer = Square(color=RED, fill_opacity=0.8).scale(1.2).shift(RIGHT * 0.5 + UP * 0.5)
        unified_label = Text("Unified Opponent Layer", color=RED).scale(0.6).next_to(unified_opp_layer, DOWN, buff=1)

        self.play(
            ReplacementTransform(opponents_6p, unified_opp_layer),
            ReplacementTransform(six_player_label, unified_label),
            run_time=2
        )
        self.wait(0.5)

        # 5. Cross-out animation over individual identities and 'Check' mark
        identities_text = Text("Individual Identities").scale(0.5).next_to(unified_label, DOWN, buff=0.5)
        self.play(Write(identities_text))
        
        # Creating a cross manually to ensure compatibility
        cross_line1 = Line(identities_text.get_corner(UL), identities_text.get_corner(DR), color=RED)
        cross_line2 = Line(identities_text.get_corner(UR), identities_text.get_corner(DL), color=RED)
        cross_group = VGroup(cross_line1, cross_line2)
        
        self.play(Create(cross_group))
        
        # Check mark over the unified 'Opponent Layer'
        checkmark = MathTex(r"\checkmark", color=GREEN).scale(1.5).next_to(unified_label, RIGHT, buff=0.3)
        self.play(Write(checkmark))

        # 6. Final Scalability Conclusion
        conclusion = Text("Same architecture for 2 or 6 players", slant="ITALIC").scale(0.5).to_edge(DOWN)
        self.play(Write(conclusion))
        
        self.wait(2)