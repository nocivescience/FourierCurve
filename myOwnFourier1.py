from manim import *
class VectorScene(Scene):
    CONFIG = {
        "n_vectors": 5,
        "vector_config": {
            "color": BLUE,
            "buff": 0,
        },
    }

    def construct(self):
        vectors = self.get_sequential_vectors()
        self.add(*vectors)
        self.wait(2)

    def get_sequential_vectors(self):
        vectors = VGroup()
        last_vector_end = ORIGIN
        for _ in range(self.CONFIG["n_vectors"]):
            vector = Vector(RIGHT, **self.CONFIG["vector_config"])
            vector.shift(last_vector_end)
            vectors.add(vector)
            last_vector_end = vector.get_end()
        return vectors