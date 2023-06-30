import numpy as np

class Noise:
    def apply(self, signal: np.ndarray) -> np.ndarray:
        pass

class AWGN(Noise):

    def __init__(self, std: float) -> None:
        super().__init__()
        self._std = std

    def apply(self, signal: np.ndarray) -> np.ndarray:
        return np.random.normal(0, self._std, size=signal.shape) + signal
