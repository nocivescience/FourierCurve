from manim import *
import functools as ft
import operator as op
class FourierCirclesScene(Scene):
    configuration = {
        'n_vectors': 5,
        'center_point': ORIGIN,
        'vector_config': {
            'buff': 0,
            'max_tip_length_to_length_ratio': 0.25,
            'tip_length': 0.15,
            'max_stroke_width_to_length_ratio': 10,
            'stroke_width': 1.7,
        },
        'slow_factor': 0.05,
        'circle_config': {
            'stroke_width': 1,
        },
        'wait_before_start': None,
    }
    def setup(self):
        Scene.setup(self)
        self.vector_clock= ValueTracker(0)
        self.add(self.vector_clock)
    def get_freqs(self):
        n= self.configuration['n_vectors']
        all_freqs= list(range(n//2,-n//2,-1))
        all_freqs.sort(key=abs)
        return all_freqs
    def get_coefficients(self):
        return [complex(0) for _ in range(self.configuration['n_vectors'])]
    def get_coefficients_of_path(self, path, n_samples=1000, freqs=None):
        if freqs is None:
            freqs= self.get_freqs()
        dt= 1/n_samples
        ts= np.arange(0,1,dt)
        sample= np.array([path.point_from_proportion(t) for t in ts])
        print(sample)
        complex_samples= sample[:,0] + 1j * sample[:,1]
        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt for freq in freqs
        ]
    def get_rotating_vectors(self, coefficients=None, freqs=None):
        vectors= VGroup()
        self.center_tracker= VectorizedPoint(self.configuration['center_point'])
        if freqs is None:
            freqs= self.get_freqs()
        if coefficients is None:
            coefficients= self.get_coefficients()
        last_vector= None
        for freq, coef in zip(freqs, coefficients):
            if last_vector is not None:
                center_function= last_vector.get_end
            else:
                center_function= self.center_tracker.get_location
            vector= self.get_rotating_vector(coef, freq, center_function)
            vectors.add(vector)
            last_vector= vector
        return vectors
    def get_rotating_vector(self, coefficient, freq, center_function):
        vector = Vector(
            RIGHT, **self.configuration['vector_config']
        )
        if abs(coefficient)==0:
            phase=0
        else:
            phase=np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_function = center_function
        vector.add_updater(
            lambda v, dt: self.update_vector(v, dt)
        )
        return vector
    def update_vector(self, vector, dt):
        tiempo = self.vector_clock.get_value()
        tiempo+=dt
        coef= vector.coefficient
        freq= vector.freq
        phase = np.log(coef).imag
        vector.set_length(abs(coef))
        vector.set_angle(phase + freq * tiempo*TAU)
        vector.shift(vector.center_function()-vector.get_start())
        return vector
    def add_vector_clock(self):
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(dt * self.configuration['slow_factor'])
        )
    def get_vector_time(self):
        return self.vector_clock.get_value()
    def get_circle(self, vector, color= BLUE_A):
        circle = Circle(
            color=color, **self.configuration['circle_config']
        )
        circle.center_func = lambda: vector.get_start()
        circle.radius_func = lambda: vector.get_length()
        circle.add_updater(
            lambda c, dt: self.update_circle(c, dt)
        )
        return circle
    def update_circle(self, circle, dt):
        circle.set(width=2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle
    def get_circles(self, vectors):
        return VGroup(*[
            self.get_circle(vector) for vector in vectors
        ])
    def get_vector_sum(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = vectors[0].get_start()
        path = ParametricFunction(
            lambda t: center + ft.reduce(op.add, [
                coef * np.exp(TAU * 1j * freq * t) for coef, freq in zip(coefs, freqs)
            ]),
            t_range=[0, 1],
            color=color,
        )
        return path
    def get_draw_path(self, vectors, stroke_width=2, color=WHITE):
        path = self.get_vector_sum(vectors, color=color)
        broken_path = CurvesAsSubmobjects(path)
        start, end = [0,1]
        def update_path(mob, dt):
            alpha = ValueTracker(0).get_value()
            n_curves = len(mob)
            for a, sp in zip(np.linspace(0, 1, n_curves), mob):
                b = alpha - a
                if b < 0:
                    width = 0
                else:
                    width = stroke_width * interpolate(start, end, 1-b%1)
                sp.set_stroke(width=width, color=color)
            return mob
        broken_path.set_color(color)
        broken_path.add_updater(update_path)
        return broken_path
class FourierScene(FourierCirclesScene):
    configuration = {
        'n_vectors': 10,
        'center_point': ORIGIN,
        'slow_factor': 0.005,
        'n_cycles': None,
        'tex_config': {
            'fill_opacity': 0,
            'stroke_width': 1,
            'stroke_color': WHITE,
        },
    }
    def construct(self):
        self.add_vectors_circles_path()
        if self.configuration['wait_before_start'] is not None:
            self.wait(self.configuration['wait_before_start'])
        self.add_vector_clock()
        self.add(self.vector_clock)
        if self.configuration['n_cycles'] is not None:
            for _ in range(self.configuration['n_cycles']):
                self.run_one_cycles()
            self.add(self.get_path())
            self.wait(10)
    def add_vectors_circles_path(self):
        path= self.get_path()
        coefs= self.get_coefficients_of_path(path)
        vectors= self.get_rotating_vectors(coefs)
        circles = self.get_circles(vectors)
        drawn_path = self.get_draw_path(vectors)
        self.add(vectors, circles, drawn_path)
    def run_one_cycles(self):
        tiempo= 1/self.configuration['slow_factor']
        self.wait(tiempo)
    def get_path(self):
        tex_mob= Tex('Ricardo', **self.configuration['tex_config'])
        tex_mob.set_height(3)
        path= tex_mob.family_members_with_points()[3]
        return path