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
    }

    def construct(self):
        vectors = self.get_sequential_vectors()
        self.add(*vectors)
        self.wait(2)

    def get_sequential_vectors(self):
        vectors = VGroup()
        last_vector_end = ORIGIN
        last_vector = None
        for i in range(self.CONFIG["n_vectors"]):
            vector = Vector(RIGHT, **self.CONFIG["vector_config"])
            vector.shift(last_vector_end)
            vectors.add(vector)
            last_vector_end = vector.get_end()
            rotation_speed = np.random.uniform(self.CONFIG["min_rotation_speed"], self.CONFIG["max_rotation_speed"])
            # Si es el penúltimo vector, añade un updater para rotarlo
            if i == self.CONFIG["n_vectors"] - 2:
                vector.add_updater(lambda v, dt, rs=rotation_speed: v.rotate(rs * dt, about_point=v.get_start()))
                last_vector = vector
            # Si es el último vector, añade un updater para moverlo al final del penúltimo vector
            elif i == self.CONFIG["n_vectors"] - 1:
                vector.add_updater(lambda v: v.shift(last_vector.get_end() - v.get_start()))
        return vectors