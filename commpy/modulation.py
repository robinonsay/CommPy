import numpy as np

class Modulation:
    def modulate(self, data: np.ndarray) -> np.ndarray:
        pass

    def demodulate(self, data: np.ndarray) -> np.ndarray:
        pass

class OOK(Modulation):

    def __init__(self, threshold, upper_bound, lower_bound) -> None:
        super().__init__()
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound
        self._threshold = threshold

    def modulate(self, data: np.ndarray) -> np.ndarray:
        return np.where(data == 1, self._upper_bound, self._lower_bound)
    
    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        return np.where(signal > self._threshold, 1, 0)
