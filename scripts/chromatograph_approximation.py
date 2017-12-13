# Import the necessary packages and modules
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import csv

# Chromatograph parameters
pre_c = 10.0
pre_d = 1.5
ramp_d = 18.0
post_c = 95.0
post_d = 1.0
final_c = 10.0
final_d = 2.5
flow_rate = 40.0
max_c = 100.0
data_format = '{:0.1f}'

# Time
dt_a = 0.0993
dt_b = 0.2087
time_a = 0
time_b = time_a + pre_d
time_c = time_b + ramp_d
time_d = time_c + post_d
time_e = time_d + final_d
time_pre_ramp = np.arange(time_a, time_b, dt_a)
time_ramp = np.arange(time_b, time_c, dt_b)
time_post_ramp = np.arange(time_c, time_d, dt_a)
time_final = np.arange(time_d, (time_e + dt_a), dt_a)
time = np.append(time_pre_ramp, time_ramp)
time = np.append(time, time_post_ramp)
time = np.append(time, time_final)

# Concentration
def find_concentration(t, m, b):
    return m*t + b

ramp_slope = ((post_c - pre_c)/ramp_d)

concentration_a_pre_ramp = find_concentration(time_pre_ramp, 0, pre_c)
concentration_a_ramp = find_concentration(time_ramp, ramp_slope, (pre_c - pre_d*ramp_slope))
concentration_a_post_ramp = find_concentration(time_post_ramp, 0, post_c)
concentration_a_final = find_concentration(time_final, 0, final_c)
concentration_a = np.append(concentration_a_pre_ramp, concentration_a_ramp)
concentration_a = np.append(concentration_a, concentration_a_post_ramp)
concentration_a = np.append(concentration_a, concentration_a_final)

concentration_b_pre_ramp = find_concentration(time_pre_ramp, 0, (max_c - pre_c))
concentration_b_ramp = find_concentration(time_ramp, -ramp_slope, ((max_c - pre_c) + pre_d*ramp_slope))
concentration_b_post_ramp = find_concentration(time_post_ramp, 0, (max_c - post_c))
concentration_b_final = find_concentration(time_final, 0, (max_c - final_c))
concentration_b = np.append(concentration_b_pre_ramp, concentration_b_ramp)
concentration_b = np.append(concentration_b, concentration_b_post_ramp)
concentration_b = np.append(concentration_b, concentration_b_final)

concentration_t_pre_ramp = concentration_a_pre_ramp + concentration_b_pre_ramp
concentration_t_ramp = concentration_a_ramp + concentration_b_ramp
concentration_t_post_ramp = concentration_a_post_ramp + concentration_b_post_ramp
concentration_t_final = concentration_a_final + concentration_b_final
concentration_t = np.append(concentration_t_pre_ramp, concentration_t_ramp)
concentration_t = np.append(concentration_t, concentration_t_post_ramp)
concentration_t = np.append(concentration_t, concentration_t_final)

# Plot the concentration
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.step(time, concentration_a, 'r-', label='a')
ax1.step(time, concentration_b, 'g-', label='b')
ax1b = ax1.twinx()
ax1b.step(time, concentration_t, 'b-', label='total')

# Style
ax1.set_xlim(0, time_e)
ax1.set_xticks(np.arange(0, (time_e + 1) ,1))
ax1.set_xlabel('time (min)')

ax1.set_ylim(0, max_c+5)
ax1.set_yticks(np.arange(0, (max_c + 5), 5))
ax1.set_ylabel('concentration (%)')

ax1b.set_ylim(0, max_c+5)
ax1b.set_yticks(np.arange(0, (max_c + 20), 20))
ax1b.set_ylabel('total concentration (%)', color='b')

ax1.legend(loc='center right')
ax1.grid()

# Volume
def find_volume(time, concentration):
    return np.cumsum(np.multiply(np.ediff1d(time,to_begin=0),concentration*flow_rate/max_c))

volume_a = find_volume(time,concentration_a)

volume_b = find_volume(time,concentration_b)

volume_t = volume_a + volume_b

# Plot the volume
ax2 = fig.add_subplot(212)
ax2.plot(time, volume_a, 'r-', label='a')
ax2.plot(time, volume_b, 'g-', label='b')
ax2b = ax2.twinx()
ax2b.plot(time, volume_t, 'b-', label='total')

# Style
ax2.set_xlim(0, time_e)
ax2.set_xticks(np.arange(0, (time_e + 1) ,1))
ax2.set_xlabel('time (min)')

max_volume = volume_a[-1]
if (volume_b[-1] > max_volume):
    max_volume = volume_b[-1]

ax2.set_ylim(0, max_volume)
ax2.set_yticks(np.arange(0, (max_volume + 25), 25))
ax2.set_ylabel('volume (ml)')

max_volume = volume_t[-1]
ax2b.set_ylim(0, max_volume)
ax2b.set_yticks(np.arange(0, (max_volume + 200), 200))
ax2b.set_ylabel('total volume (ml)', color='b')

ax2.legend(loc='center right')
ax2.grid()

# Show the plot
fig.tight_layout()
plt.suptitle('HPLC Chromatograph Dec 11 2017')
plt.show()

# Save the data

with open('../data/theory_approximation.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile)
    spamwriter.writerow(['time',
                         'concentration a (%)',
                         'concentration b (%)',
                         'concentration total (%)',
                         'volume a (ml)',
                         'volume b (ml)',
                         'volume total (ml)',
    ])
    for t in np.arange(0, time[-1], 1):
        spamwriter.writerow([data_format.format(t),
                             data_format.format(np.interp(t,time,concentration_a)),
                             data_format.format(np.interp(t,time,concentration_b)),
                             data_format.format(np.interp(t,time,concentration_t)),
                             data_format.format(np.interp(t,time,volume_a)),
                             data_format.format(np.interp(t,time,volume_b)),
                             data_format.format(np.interp(t,time,volume_t)),
        ])
