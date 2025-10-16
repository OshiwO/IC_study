from fff import nfff

import numpy as np
import matplotlib.pyplot as plt

###
VCC = 1.8
simulation_length = 400
time = np.linspace(0,5e-4,simulation_length)

## external circuit introduction
R_1 = 2000
R_2 = 20000
C = 3.3e-9
Charge_constant = C * (R_1 + R_2)
DIS_constant = C * R_2

voltage_initial = 0


### 实例化555芯片
THR = 1.5
TRI = 1.5
chip = nfff(THR,TRI,0,0,0,VCC)

### pre running
voltage = np.zeros(400)
voltage_m = np.zeros(400)
Output = np.zeros(simulation_length)
t = 0
SIGN = chip.DIS
for h in range(simulation_length):
    if SIGN != chip.DIS:
        t = 0
        SIGN = chip.DIS
    if SIGN == 0:
        voltage_m[t] = VCC*1/3 + VCC * (1 - np.exp(-time[t] / Charge_constant))
    if SIGN == 1:
        voltage_m[t] = VCC*2/3 - VCC * (1 - np.exp(-time[t] / DIS_constant))

    voltage[h] = voltage_m[t]
    t = t + 1
    chip.THR = voltage[h]
    chip.TRI = voltage[h]
    chip.run()
    Output[h] = chip.Out


plt.plot(time, Output)
plt.show()
