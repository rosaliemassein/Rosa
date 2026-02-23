from manim import *

class PseudoExecutionEfficiency(Scene):
    def construct(self):
        self.set_camera_position(ORIGIN, ORIGIN, 1.5)
        
        # Traditional AutoML
        traditional = Text(
            "Traditional AutoML",
            color=RED,
            font="Roboto Mono",
        )
        traditional.set_opacity(0.5)
        
        loading_wheel = SVGMobject(r"""
            <svg width="40" height="40">
                <circle cx="20" cy="20" r="15" stroke="black" fill="none"/>
                <path d="M20,20 A15,15 0 0 1 18.65,22.98
                15,15 0 0 1 21.35,22.98
                15,15 0 0 1 20,20"
                 stroke="white" stroke-width="2"/>
            </svg>
        """)
        loading_wheel.scale(0.5)
        
        bar_chart = [
            Line(ORIGIN, ORIGIN + 1.5, color=BLUE)
        ]
        
        traditional_group = VGroup(traditional, loading_wheel).arrange(RIGHT)
        bar_chart_group = [bar_chart[0]]
        
        self.play(Create(traditional_group), Create(bar_chart_group))
        self.wait(2)
        
        # "Search for the best model usually requires training dozens of candidates, which is incredibly slow."
        text1 = Text(
            "Searching for the best model usually requires training dozens of candidates, which is incredibly slow.",
            color=YELLOW,
            font="Cascadia Mono",
        )
        self.play(FadeIn(text1))
        self.wait(3)
        
        # AutoML-Agent
        auto_ml_agent = ImageMobject("img-1.jpeg")
        
        # Remarks: Demonstrate 'training-free search'
        remarks = Text(
            "To speed things up, AutoML-Agent performs 'training-free search.' The Data and Model agents use their inherent knowledge to simulate or 'pseudo-execute' the plan. They estimate outcomes like accuracy and inference speed without actually writing or running code yet. This allows the system to narrow down thousands of possibilities to the best few in seconds.",
            color=WHITE,
            font="Cascadia Mono",
        )
        remarks.scale(0.8)
        
        self.play(TransformMatchingShapes(traditional_group, [auto_ml_agent]))
        self.wait(3)
        
        # "Visualize the efficiency of predicting performance metrics through LLM knowledge instead of actual training."
        text2 = Text(
            "Visualize the efficiency of predicting performance metrics through LLM knowledge instead of actual training.",
            color=WHITE,
            font="Cascadia Mono",
        )
        text2.scale(0.8)
        
        self.play(FadeIn(text2))
        self.wait(3)
        
        # "Show a 'Traditional AutoML' side with a slow-spinning loading wheel and a bar chart barely growing."
        traditional_group[1].set_opacity(0.5)
        
        self.play(TransformMatchingShapes(bar_chart_group, []))
        self.wait(3)
        
        # "On the 'AutoML-Agent' side, show a 'Brain' icon (LLM) flashing quickly, instantly generating a table of results including 'Accuracy: 95%' and 'Latency: 10ms'. Use TransformMatchingShapes to turn a list of 'Candidate Models' into a 'Ranked Leaderboard' instantly."
        ldm = ImageMobject("img-1.jpeg")
        
        table = VGroup(
            MathTex(r"Accuracy: 95%"),
            MathTex(r"Latency: 10ms"),
        ).arrange(DOWN, buff=0.2)
        
        leaderboard = VGroup(
            MathTex("Model 1"),
            MathTex("Model 2"),
            MathTex("Model 3"),
        ).arrange(DOWN, buff=0.2).next_to(ORIGIN, RIGHT)
        
        self.play(TransformMatchingShapes(auto_ml_agent, [ldm]))
        self.wait(3)
        
        self.play(FadeIn(table))
        self.wait(2)
        
        self.play(TransformMatchingShapes(leaderboard, []))
        self.wait(3)
        
        # Formula
        formula = Text(
            r"$O_{i}^{m} = \mathcal{A}_{m}(\mathbf{s}_{i}^{m})$",
            color=WHITE,
            font="Cascadia Mono",
        )
        formula.scale(0.8)
        
        self.play(TransformMatchingShapes(table, [formula]))
        self.wait(3)

        # Show the final outcome
        final_leaderboard = VGroup(
            MathTex("Model 1 (Accuracy: 95%, Latency: 10ms)"),
            MathTex("Model 2 (Accuracy: 94%, Latency: 10ms)"),
            MathTex("Model 3 (Accuracy: 93%, Latency: 10ms)"),
        ).arrange(DOWN, buff=0.2).next_to(ORIGIN, RIGHT)
        final_formula = Text(
            r"$O_{i}^{m} = \mathcal{A}_{m}(\mathbf{s}_{i}^{m})$",
            color=WHITE,
            font="Cascadia Mono",
        )
        
        self.play(TransformMatchingShapes(leaderboard, final_leaderboard))
        self.wait(3)
        
        self.play(TransformMatchingShapes(formula, final_formula))
        self.wait(3)