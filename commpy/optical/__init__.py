import numpy as np
import commpy
from typing import Union

def pwr_to_irradiance(pwr: Union[np.ndarray, float], distance: Union[np.ndarray, float], divergence: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
    return pwr - commpy.dec_to_db(np.pi * (np.tan(divergence / 2) * distance)**2)
