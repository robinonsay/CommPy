import numpy as np
import commpy
import json
from typing import Union, NamedTuple

def pwr_to_irradiance(pwr: Union[np.ndarray, float], distance: Union[np.ndarray, float], divergence: Union[np.ndarray, float]) -> Union[np.ndarray, float]:
    return pwr - commpy.lin_to_db(np.pi * (np.tan(divergence / 2) * distance)**2)

def beam_divergence(wavelength: Union[np.ndarray, float], beam_waist: Union[np.ndarray, float])-> Union[np.ndarray, float]:
    return wavelength / (np.pi * beam_waist)

class Laser(NamedTuple):
    wavelength: Union[np.ndarray, float]
    power: Union[np.ndarray, float]
    beam_divergence: Union[np.ndarray, float]

    def __str__(self) -> str:
        d = dict()
        for key, value in zip(self._fields, self):
            d[key] = value
        return json.dumps(d, indent=4)

class Photodiode(NamedTuple):
    wavelength: Union[np.ndarray, float]
    active_area: Union[np.ndarray, float]
    nep: Union[np.ndarray, float]

    def __str__(self) -> str:
        d = dict()
        for key, value in zip(self._fields, self):
            d[key] = value
        return json.dumps(d, indent=4)

class Receiver(NamedTuple):
    photodiode: Photodiode
    bit_rate: Union[np.ndarray, float]
    bandwidth: Union[np.ndarray, float]
    aperture: float
    spot: float
    error: Union[np.ndarray, float]

    def __str__(self) -> str:
        d = dict()
        for key, value in zip(self._fields, self):
            d[key] = value
        return json.dumps(d, indent=4)

    @property
    def min_snr(self):
        return np.exp2(self.bit_rate/self.bandwidth) - 1

    @property
    def min_irradiance(self):
        min_irr = self.photodiode.nep * np.sqrt(self.bandwidth) * self.min_snr / self.photodiode.active_area
        lens_gain = (self.aperture/self.spot)**2 * self.error
        return min_irr / lens_gain
    
    @property
    def min_irradiance_db(self):
        return commpy.lin_to_db(self.min_irradiance)


def calc_range(pwr, divergence, min_irradiance_db, start, threshold=1):
    delta = start / 2
    r = start
    while delta > threshold:
        if pwr_to_irradiance(pwr, r, divergence) > min_irradiance_db:
            r += delta
        else:
            delta /= 2
            r -= delta
    return r
