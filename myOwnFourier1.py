from manim import *
class VectorScene(Scene):
    CONFIG = {
        "n_vectors": 5,
        "vector_config": {
            "color": BLUE,
            "buff": 0,
        },
        "min_rotation_speed": 0.5,  # Velocidad de rotación mínima
        "max_rotation_speed": 1.5,  # Velocidad de rotación máxima
        'center_point': ORIGIN,
    }

    def construct(self):
        vectors = self.get_sequential_vectors()
        self.add(*vectors)
        self.wait(2)

    def get_sequential_vectors(self):
        vectors = VGroup()
        last_vector = None
        for i in range(self.CONFIG["n_vectors"]):
            vector = Vector(RIGHT, **self.CONFIG["vector_config"])
            if last_vector is None:
                last_vector = self.CONFIG['center_point']
            else:
                last_vector = vector.get_end()
            vector.rotate(
                np.random.uniform(0, TAU),
                about_point=last_vector
            )
            vector.move_to(last_vector)
            print(last_vector)
            vector.add_updater(lambda v, dt: v.rotate(
                np.random.uniform(
                    self.CONFIG["min_rotation_speed"],
                    self.CONFIG["max_rotation_speed"]
                ) * dt, about_point=last_vector
            ))  
            vector.add_updater(lambda v: v.shift(last_vector - v.get_start()))
            vectors.add(vector)
            last_vector = vector.get_end()
        return vectors