import numpy as np
import matplotlib.pyplot as plt
import commpy
from commpy import optical
from commpy import modulation
from commpy import noise

DISTANCE = 340E3  # 340km to the ISS
WAVELENGTH = 850E-9
BANDWIDTH = 850E6
LASER = optical.Laser(wavelength=WAVELENGTH,
                      power=3E-3,
                      beam_divergence=1.2E-3)
PHOTODIODE = optical.Photodiode(wavelength=WAVELENGTH,
                                active_area=7.02* 1E-6,
                                nep=41E-15)
RECEIVER = optical.Receiver(photodiode=PHOTODIODE,
                            bit_rate=BANDWIDTH * 2,
                            bandwidth=BANDWIDTH,
                            aperture=34E-3,
                            spot=3.2E-6,
                            error=0.9)
ATMOSPHERE_ATTENUATION_BIAS_DB = 40
ATMOSPHERE_ATTENUATION_DB = -commpy.lin_to_db(0.801) + ATMOSPHERE_ATTENUATION_BIAS_DB  # MODTRAN derived value 80.1% at 850nm through atmosphere
print(f"Min Irradiance (dB): {RECEIVER.min_irradiance_db}")
print(f"Min SNR (dB): {commpy.lin_to_db(RECEIVER.min_snr)}")
print(f"Atmospheric Attenuation (dB): {ATMOSPHERE_ATTENUATION_DB}")

atm_att_pwr = LASER.power - ATMOSPHERE_ATTENUATION_DB
rx_irradiance = optical.pwr_to_irradiance(atm_att_pwr, DISTANCE, LASER.beam_divergence)
if rx_irradiance >= RECEIVER.min_irradiance_db:
    print(f"PASS: Link Margin of {rx_irradiance - RECEIVER.min_irradiance_db:.3f} dB")

else:
    print(f"Fail: RX irradiance {commpy.db_to_dbm(rx_irradiance):.3f} dBm < RX min irradiance {commpy.db_to_dbm(RECEIVER.min_irradiance_db):.3f} dBm")
print(f"Range: {optical.calc_range(atm_att_pwr, LASER.beam_divergence, RECEIVER.min_irradiance_db, DISTANCE) / 1E3:.3f} km")
