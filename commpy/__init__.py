import numpy as np
from typing import Union

def link_margin(gains: np.ndarray, losses: np.ndarray) -> float:
    return gains.sum() - losses.sum()

def dec_to_db(val: Union[np.ndarray, float], ref=1) -> Union[np.ndarray, float]:
    return 10 * np.log10(val/ref)

def db_to_dec(val: Union[np.ndarray, float], ref=1) -> Union[np.ndarray, float]:
    return 10**(val / 10) * ref

def db_to_dbm(val: Union[np.ndarray, float]):
    return val + 30


def fspl(wavelength: Union[np.ndarray, float], distance: Union[np.ndarray, float], tx_gain=0, rx_gain=0) -> Union[np.ndarray, float]:
    return tx_gain + rx_gain + 20 * np.log10(wavelength / (4 * np.pi * distance))
