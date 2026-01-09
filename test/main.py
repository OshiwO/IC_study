from RSLATCH import RSLATCH

import numpy as np
import matplotlib.pyplot as plt


## simple test for git
R_1 = 2000
R_2 = 20000
C = 3.3e-9
Charge_constant = C * (R_1 + R_2)
DIS_constant = C * R_2
time = np.linspace(0,5e-4,400)
voltage_initial = 0


t = 0
SIGN = 1
voltage = np.zeros(400)
voltage_m = np.zeros(400)

class COMP:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        self.Out = 0
    def run(self):
        if(self.a >= self.b):
            self.Out = 1
        else:
            self.Out = 0

C = COMP(1,0)
C.run()
print(C.Out)
VCC = 1.8

### 定义555芯片内部
class fff:
    def __init__(self,IN1,VH,VL,IN2,DIS):
        self.IN1 = IN1
        self.IN2 = IN2
        self.VH = VH
        self.VL = VL

        self.Vc1 = COMP(IN1,VH)             ### 比较器1
        self.Vc2 = COMP(VL,IN2)             ### 比较器2 

        self.Vrs = RSLATCH(self.Vc1,self.Vc2)   ### 锁存器

        self.DIS = DIS
        self.Out = 0
    def run(self):                          ### 运行
        self.Vc1.a = self.IN1
        self.Vc2.b = self.IN2
        self.Vc1.run()
        self.Vc2.run()
        self.Vrs.R = self.Vc1.Out
        self.Vrs.S = self.Vc2.Out
        self.Vrs.run(self.Vrs.R, self.Vrs.S)
        self.DIS = self.Vrs.NOut
        self.Out = self.Vrs.Out
        

## 对于电容充电放电的解释

x = [0,0.5,0.7,1,2,3,4,5]
volt = 1-1/np.exp(x)
curr = 1/np.exp(x)

### 首先进行一个外部电路的设计
### 外部电路包括电容与两个电路，其中高电位用于给电路放电，低电位用于给电压充电

### 首先模拟外部电路中电阻与电容的充放电情况

'''
for i in range(400):
    if voltage[i-1] > 2/3* VCC:   ### 判断 比较器1 状态
        SIGN = -1
        t = 1
    if voltage[i-1] < 1/3 * VCC:  ### 判断 比较器2 状态
        SIGN = 1
        t = 1
    if SIGN == 1:
        voltage[i] = 0.6 + VCC * (1 - np.exp(-time[t] / Charge_constant))
    if SIGN == -1:
        voltage[i] = 1.2 - VCC * (1 - np.exp(-time[t] / DIS_constant))
    t = t + 1

plt.plot(time, voltage)             ### 电压信号的变化，直接代表了555芯片外部电路的充放电
plt.show()
'''

### 实例化一个555
t = 0
test = fff(0, 1.5, 0.200000, 0, 0)  #IN1,VH,VL,IN2,DIS
out_a = np.zeros(400)
out_b = np.zeros(400)
SIGN = test.DIS
for h in range(400):
    if SIGN != test.DIS:
        t = 0
        SIGN = test.DIS
    if SIGN == 0:
        voltage_m[t] = 0.2 + VCC * (1 - np.exp(-time[t] / Charge_constant))
    if SIGN == 1:
        voltage_m[t] = 1.5 - VCC * (1 - np.exp(-time[t] / DIS_constant))

    voltage[h] = voltage_m[t]
    t = t + 1
    test.IN1 = voltage[h]
    test.IN2 = voltage[h]
    test.run()
    out_a[h] = test.Out
    out_b[h] = test.Vc2.Out
print(t)
plt.plot(time, out_a)
plt.show()
