from manim import *
import itertools as it
class FourierCurve1(Scene):
    dicc1 = {
        'n_vectors': 10,
        'big_radius': 2,
        'colors': [BLUE, GREEN, RED, ORANGE, YELLOW,],
        'vector_config': {
            'stroke_width': 2,
            'max_tip_length_to_length_ratio': 0.1,
        },
        'tex_config': {
            'fill_opacity': 0,
            'stroke_width': 1,
            'stroke_color': WHITE,
        },
        'center_point': ORIGIN,
    }
    def construct(self):
        self.add_vector_circles()
    def add_vector_circles(self):
        path= self.get_path()
        coefs= self.get_coeffcients_of_path(path)
        vectors= self.get_rotating_vectors(coefs)
        self.add(path, vectors)
        self.wait(2)
    def get_path(self):
        text_mob= Text('F', **self.dicc1['tex_config'])
        text_mob.set(height=5)
        path= text_mob.family_members_with_points()[0]
        return path
    def get_freqs(self):
        n= self.dicc1['n_vectors']
        all_freqs= list(range(n//2, -n//2, -1))
        all_freqs.sort(key= lambda x: abs(x))
        return all_freqs
    def get_coeffcients(self):
        return [
            complex(0) for _ in range(self.dicc1['n_vectors'])
        ]
    def get_coeffcients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs= self.get_freqs()
        dt= 1/n_samples
        ts= np.arange(0, 1, dt)
        samples = np.array([path.point_from_proportion(t) for t in ts])
        samples-= self.dicc1['center_point']
        complex_samples= samples[:, 0]+1j*samples[:, 1]
        return [
            np.array([
                np.exp(-TAU*1j*freq*t)*complex_sample
                for t, complex_sample in zip(ts, complex_samples)
            ]).sum()*dt for freq in freqs
        ]
    def get_rotating_vectors(self, freqs=None, coefficients=None, color=BLUE_A):
        vectors= VGroup()
        self.center_tracker= VectorizedPoint(self.dicc1['center_point'])
        if freqs is None:
            freqs= self.get_freqs()
        if coefficients is None:
            coefficients= self.get_coeffcients()
        last_vector= None
        for freq, coef, color in zip(freqs, coefficients, it.cycle(self.dicc1['colors'])):
            if last_vector:
                center_func= last_vector.get_end
            else:
                center_func= self.center_tracker.get_location
            vector= self.get_rotating_vector(
                freq=freq,
                coef=coef,
                center_func=center_func,
                color=color
            )
            vectors.add(vector)
            last_vector=vector
        return vectors
    def get_rotating_vector(self, freq, coef, center_func,color):
        vector =Vector(RIGHT, **self.dicc1['vector_config'])
        vector.scale(abs(coef))
        vector.set_color(color)
        if abs(coef)==0:
            phase= 0
        else:
            # phase= np.angle(coef)
            phase= np.log(coef).imag
        vector.rotate(phase, about_point= ORIGIN)
        vector.freq= freq
        vector.coef= coef
        vector.center_func= center_func
        vector.add_updater(self.update_vector)
        return vector
    def update_vector(self, vector, dt):
        time=0
        coef=vector.coef
        freq=vector.freq
        phase= np.log(coef).imag
        vector.set_length(abs(coef))
        vector.set_angle(phase+time*freq*TAU)
        vector.shift(vector.center_func()-vector.get_start())
        return vector