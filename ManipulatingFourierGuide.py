from manim import *
import itertools as it 
import operator as op
import functools as ft
class AbstractFourierOfTexSymbol(ZoomedScene):
    CONFIG = {
        "n_vectors": 10,
        "center_point": ORIGIN,
        "n_cycles": None,
        "tex": r"\rm M",
        "start_drawn": True,
        "path_custom_position": lambda mob: mob,
        "max_circle_stroke_width": 1,
        "tex_class": MathTex,
        "tex_config": {
            "fill_opacity": 0,
            "stroke_width": 1,
            "stroke_color": WHITE
        },
        "big_radius": 2,
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.25,
            "tip_length": 0.15,
            "max_stroke_width_to_length_ratio": 10,
            "stroke_width": 1.7,
        },
        "circle_config": {
            "stroke_width": 1,
        },
        "slow_factor": 0.5,
    }
    def setup(self):
        ZoomedScene.setup(self)
        self.slow_factor_tracker = ValueTracker(
            self.CONFIG["slow_factor"]
        )
        self.vector_clock = ValueTracker(0)
        self.add(self.vector_clock)
    def construct(self):
        # This is not in the original version of the code.
        self.add_vectors_circles_path()
        self.wait(2)
 
    def add_vectors_circles_path(self):
        path = self.get_path()
        # self.path_custom_position(path)
        coefs = self.get_coefficients_of_path(path)
        vectors = self.get_rotating_vectors(coefficients=coefs)
        self.add(path)
        self.add(vectors)
 
        self.vectors = vectors
        self.path = path
 
    def get_path(self):
        tex_mob = self.CONFIG['tex_class'](self.CONFIG['tex'], **self.CONFIG['tex_config'])
        tex_mob.set_height(6)
        path = tex_mob.family_members_with_points()[0]
        return path
    def add_vector_clock(self):
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(
                self.get_slow_factor() * dt
            )
        )
 
    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()
 
    def get_vector_time(self):
        return self.vector_clock.get_value()
 
    def get_freqs(self):
        n = self.CONFIG["n_vectors"]
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs
 
    def get_coefficients(self):
        return [complex(0) for _ in range(self.CONFIG["n_vectors"])]
 
    def get_color_iterator(self):
        return it.cycle(self.CONFIG["colors"])
 
    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(self.CONFIG["center_point"])
 
        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()
 
        last_vector = None
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func,
            )
            vectors.add(vector)
            last_vector = vector
        return vectors
 
    def get_rotating_vector(self, coefficient, freq, center_func):
        vector = Vector(RIGHT, **self.CONFIG["vector_config"])
        vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_vector)
        return vector
 
    def update_vector(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag
 
        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector
 
    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= self.CONFIG["center_point"]
        complex_samples = samples[:, 0] + 1j * samples[:, 1]
 
        return [
            np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt for freq in freqs
        ]