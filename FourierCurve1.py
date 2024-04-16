from manim import *
import itertools as it
class FourierCurve1(Scene):
    dicc1 = {
        'n_vectors': 10,
        'big_radius': 2,
        'colors': [BLUE, GREEN, RED, ORANGE, YELLOW,],
        'vector_config': {
            'stroke_width': .2,
            'max_tip_length_to_length_ratio': 0.1,
            'buff':0
        },
        'tex_config': {
            'fill_opacity': 0,
            'stroke_width': 1,
            'stroke_color': WHITE,
        },
        'center_point': ORIGIN,
    }
    def construct(self):
        self.add_vector_circles_path()
    def add_vector_circles_path(self):
        path= self.get_path()
        coef= self.get_coefficients_of_path(path)
        vectors= self.get_rotating_vectors(coefficients=coef)
        self.add(path, vectors)
        self.wait(5)
    def get_path(self):
        text_mob= Text('F', **self.dicc1['tex_config'])
        text_mob.set(height=5)
        path= text_mob.family_members_with_points()[0]
        return path
    def get_coefficients_of_path(self, path, n_samples=1000, freqs=None):
        if freqs is None:
            freqs= self.get_freqs()
        dt= 1/n_samples
        ts= np.arange(0, 1, dt)
        samples= np.array([path.point_from_proportion(t) for t in ts])
        samples-= self.dicc1['center_point']
        complex_samples= samples[:, 0] + 1j*samples[:, 1]
        return [
            np.array([
                np.exp(-TAU*1j*freq*t)*cs for t, cs in zip(ts, complex_samples)
            ]).sum()*dt for freq in freqs
        ]
    def get_freqs(self):
        n= self.dicc1['n_vectors']
        all_freqs= list(range(n//2,-n//2,-1))
        all_freqs.sort(key=abs)
        return all_freqs
    def get_coefficients(self):
        return [complex(0) for _ in range(self.dicc1['n_vectors'])]
    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors= VGroup()
        self.center_tracker= VectorizedPoint(self.dicc1['center_point'])
        if freqs is None:
            freqs= self.get_freqs()
        if coefficients is None:
            coefficients= self.get_coefficients()
        last_vector= None
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector:
                center_point= last_vector.get_end()
            else:
                center_point= self.center_tracker.get_location()
            vector= self.get_rotating_vector(coefficient, freq, center_point)
            vectors.add(vector)
            last_vector= vector
        return vectors
    def get_rotating_vector(self, coefficient, freq, center_point):
        vector = Vector(
            RIGHT,
            **self.dicc1['vector_config']
        )
        vector.scale(abs(coefficient))
        if(abs(coefficient) ==0):
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=center_point)
        vector.coefficient = coefficient
        vector.freq = freq
        vector.center_point = center_point
        vector.add_updater(self.update_vector)
        vector.shift(center_point)
        return vector
    def update_vector(self, vector, dt):
        time=0
        coefficient= vector.coefficient
        freq= vector.freq
        center_point= vector.center_point
        phase= np.log(coefficient).imag
        vector.set_length(abs(coefficient))
        vector.set_angle(phase+time*TAU*freq)
        vector.shift(vector.center_point-vector.get_start())