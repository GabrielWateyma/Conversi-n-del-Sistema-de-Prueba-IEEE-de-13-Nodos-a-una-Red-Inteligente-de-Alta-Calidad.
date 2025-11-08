import numpy as np

hourly_irradiance_Wh_m2 = [
    64, 287, 507, 534, 515, 830, 813 
]

minute_counts = [60, 60, 60, 60, 60, 60, 4]

PV_SYSTEM_CAPACITY_KW = 280 
IRRADIANCE_STC = 1000       
HOURS_PER_STEP = 1          

expanded_irradiance_W_m2 = []

for Wh_m2_per_hour, count in zip(hourly_irradiance_Wh_m2, minute_counts):
    avg_irradiance_W_m2 = Wh_m2_per_hour / HOURS_PER_STEP
    expanded_irradiance_W_m2.extend([avg_irradiance_W_m2] * count)

pv_power_kW = []
for W_m2 in expanded_irradiance_W_m2:
    scaling_factor = W_m2 / IRRADIANCE_STC
    power_output = scaling_factor * PV_SYSTEM_CAPACITY_KW
    pv_power_kW.append(power_output)

npts_final = len(pv_power_kW) 

dss_mult_line = f'~ mult=('
for i, kw in enumerate(pv_power_kW):
    dss_mult_line += f'{kw:.3f} '
    
    if (i + 1) % 10 == 0 and i < npts_final - 1:
        dss_mult_line += '\n~ '

dss_mult_line += ')'

dss_code = f"""
New Loadshape.PV_Profile_364 npts={npts_final} interval=1m
{dss_mult_line}
"""

print(dss_code)