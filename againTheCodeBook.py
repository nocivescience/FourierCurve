from manim import *
class FourierScene(Scene):
    dicc={
        'n_vectors':10,
        'vector_config':{
            'buff':0,
            'max_tip_length_to_length_ratio':0.25,
            'max_stroke_width_to_length_ratio':0.2,
        },
        'center_point':ORIGIN,
    }
    def construct(self):
        self.add_rotating_vectors()
    def add_rotating_vectors(self):
        vectors=self.get_rotating_vectors()
        self.add(*vectors)
        self.wait(2)
    def get_rotating_vectors(self):
        vectors=VGroup()
        coef=self.get_coefs()
        freqs=self.get_freqs()
        self.center_tracker=VectorizedPoint(self.dicc['center_point'])
        last_vector=None
        for c, f in zip(coef, freqs):
            if last_vector is None:
                last_vector=self.center_tracker
            else:
                last_vector=last_vector.get_end()
            vector=self.get_rotating_vector(c, f, lambda: self.center_tracker.get_location())
            print(last_vector)
            vectors.add(vector)
            last_vector=vector
        return vectors
    def get_freqs(self):
        n=self.dicc['n_vectors']
        all_freqs= list(range(n//2, -n//2, -1))
        all_freqs.sort(key=abs)
        return all_freqs
    def get_coefs(self):
        return [complex(0) for _ in range(self.dicc['n_vectors'])]
    def get_rotating_vector(self, coefficient, freq, center_func):
        vector=Vector(RIGHT, **self.dicc['vector_config'])
        vector.scale(abs(coefficient))
        if abs(coefficient)==0:
            return vector
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=center_func)
        vector.coefficient=coefficient
        vector.freq=freq
        vector.center_func=center_func
        vector.add_updater(lambda v, dt: self.update_vectors(v, dt))
        return vector
    def update_vectors(self, vector, dt):
        time=0
        coef=vector.coefficient
        freq=vector.freq
        center_func=vector.center_func
        phase = np.log(coef).imag
        vector.set_length(abs(coef))
        vector.set_angle(phase+time*freq*TAU)
        vector.shift(center_func()-vector.get_start())
        return vector