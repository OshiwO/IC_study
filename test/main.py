from RSLATCH import RSLATCH

import numpy as np
import matplotlib.pyplot as plt


## simple test for git


class COMP:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        self.Out = 1
    def run(self):
        if(self.a >= self.b):
            self.Out = 1
        else:
            self.Out = 0

C = COMP(1,0)
C.run()
print(C.Out)
VCC = 1.8

class fff:
    def __init__(self,IN1,VH,VL,IN2,DIS):
        self.IN1 = IN1
        self.IN2 = IN2
        self.VH = VH
        self.VL = VL

        self.Vc1 = COMP(IN1,VH)
        self.Vc2 = COMP(VL,IN2)

        self.Vrs = RSLATCH(self.Vc1,self.Vc2)

        self.DIS = DIS
        self.Out = 0
    def run(self):
        self.Vc1.a = self.IN1
        self.Vc2.b = self.IN2
        self.Vc1.run()
        self.Vc2.run()
        self.Vrs.R = self.Vc1.Out
        self.Vrs.S = self.Vc2.Out
        self.Vrs.run()
        self.Out = not self.Vrs.Out

## 对于电容充电放电的解释

x = [0,0.5,0.7,1,2,3,4,5]
volt = 1-1/np.exp(x)
curr = 1/np.exp(x)

### 首先进行一个外部电路的设计
### 外部电路包括电容与两个电路，其中高电位用于给电路放电，低电位用于给电压充电

### 首先模拟外部电路中电阻与电容的充放电情况

R_1 = 2000
R_2 = 20000
C = 10e-9
Charge_constant = C * (R_1 + R_2)
DIS_constant = C * R_2
time = np.linspace(0,5e-4,400)
voltage_initial = 0


t = 0
SIGN =1
voltage = np.ones(400)
for i in range(400):
    if voltage[i-1] > 2/3* VCC:
        SIGN = -1
        t = 1
    if voltage[i-1] < 1/3 * VCC:
        SIGN = 1
        t = 1
    if SIGN == 1:
        voltage[i] = 0.6 + VCC * (1 - np.exp(-time[t] / Charge_constant))
    if SIGN == -1:
        voltage[i] = 1.2 - VCC * (1 - np.exp(-time[t] / DIS_constant))
    t = t + 1
print(voltage)
plt.plot(time, voltage)
plt.show()
### 实例化一个555

test = fff(0,1.20000,0.600000,0,0)  #IN1,VH,VL,IN2,DIS
out = np.zeros(400)
for h in range(400):
    test.IN1 = voltage[h]
    test.IN2 = voltage[h]
    test.run()
    out[h] = test.Vc1.Out

print(out)
plt.plot(time, out)
plt.show()