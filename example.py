import numpy as np
import matplotlib.pyplot as plt
import commpy
from commpy import optical
from commpy import modulation
from commpy import noise

'''
The Laser: https://www.quarton.com/uploadfiles/1028/product/IR-laser-modules/VLM-850-03-series/IR-Dot-Laser-Module-VLM-850-03-Manual.pdf
The Receiver: https://www.ttelectronics.com/TTElectronics/media/ProductFiles/Datasheet/OPL800.pdf
'''

DISTANCE = 340E3  # 340km to the ISS
TX_PWR = commpy.dec_to_db(3E-3)  # 1.5 mW Laser
WAVELENGTH = 850E-9  # 850 nm laser
RX_MIN_IRRADIANCE_DB= commpy.dec_to_db(2E-6 * 10E3)  # 2 uW/cm^2 min irradiance of the receiver (in W/m^2)
BEAM_DIVERGENCE = 1.2E-3 * 2  # 1.2 mRad
ATMOSPHERE_ATTENUATION_DB = 10*np.log10(0.6)  # MODTRAN derived value 80.1% at 850nm through atmosphere

pwr = TX_PWR + ATMOSPHERE_ATTENUATION_DB
rx_irradiance = optical.pwr_to_irradiance(pwr, DISTANCE, BEAM_DIVERGENCE)
def calc_range(tx_pwr, start, threshold=1):
    delta = start / 2
    r = start
    while delta > threshold:
        if optical.pwr_to_irradiance(tx_pwr, r, BEAM_DIVERGENCE) > RX_MIN_IRRADIANCE_DB:
            r += delta
        else:
            delta /= 2
            r -= delta
    return r

if rx_irradiance >= RX_MIN_IRRADIANCE_DB:
    print(f"PASS: Link Margin of {commpy.db_to_dbm(rx_irradiance) - commpy.db_to_dbm(RX_MIN_IRRADIANCE_DB):.3f} dBm")
    data = np.random.randint(0, 2, 2**15)
    LOWER_BOUND = -100
    modulator = modulation.OOK(RX_MIN_IRRADIANCE_DB, TX_PWR, lower_bound=LOWER_BOUND)
    channel = noise.AWGN(std=1.5)
    tx_signal = modulator.modulate(data)
    rx_signal = channel.apply(optical.pwr_to_irradiance(tx_signal+ ATMOSPHERE_ATTENUATION_DB, DISTANCE, BEAM_DIVERGENCE))
    rx_signal[rx_signal < LOWER_BOUND] = LOWER_BOUND
    rx_data = modulator.demodulate(rx_signal)
    ber = np.where(data != rx_data, 1, 0).sum() / len(data)
    print(f"BER: {ber}")
    plt.plot(tx_signal[:25])
    plt.plot(rx_signal[:25])
    plt.show()
else:
    print(f"Fail: RX irradiance {commpy.db_to_dbm(rx_irradiance):.3f} dBm < RX min irradiance {commpy.db_to_dbm(RX_MIN_IRRADIANCE_DB):.3f} dBm")
print(f"Range: {calc_range(pwr, 100) / 1E3:.3f} km")


