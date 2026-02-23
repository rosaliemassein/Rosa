from manim import *

class IterativeClusteringConcept(Scene):
    def construct(self):
        # Create a 3x9 grid of dots
        dots = VGroup(*[
            Dot(color=BLUE) for _ in range(27)
        ]).arrange_in_grid(rows=3, cols=9)

        # Highlight the two closest dots initially
        initial_dots = VGroup(
            Dot(color=RED).next_to(dots[0], direction=UP),
            Dot(color=GREEN).next_to(dots[1], direction=RIGHT)
        )

        # Draw a search circle around the initial pair
        search_circle = Circle(
            color=ORANGE,
            radius=1.5,
            fill_opacity=0
        ).move_to(initial_dots.get_center()).grow_animated(ani_duration=2)

        self.add(dots)
        self.play(Create(search_circle), run_time=2)
        
        # Function to find the next closest dot
        def get_next_closest_dot(dots, search_circle):
            distances = [dot.get_distance(search_circle) for dot in dots]
            closest_dot_index = distances.index(min(distances))
            return dots[closest_dot_index]

        # Main cluster assignment loop
        clusters = 3
        for i in range(clusters):
            self.add(initial_dots[0], initial_dots[1])
            
            while len(dots) > 0:
                closest_dot = get_next_closest_dot(dots, search_circle)
                closest_dot.set_color(initial_dots[0].get_color())
                dots.remove(closest_dot)
            
            # Update search circle position for the next cluster
            if i < clusters - 1:
                search_circle.move_to(initial_dots[0].get_center())
                search_circle.grow_animated(ani_duration=1)
            
            self.add(search_circle)

        # Final position of search circle
        self.play(FadeOut(initial_dots), run_time=2)
        self.wait()

        # Narration
        self.play(Write(Text("This iterative approach ensures each group of nine proposals has the highest possible thematic cohesion, making it easier to find a single panel of reviewers who can cover the whole batch.", color=WHITE).scale(0.7)))
        self.wait()