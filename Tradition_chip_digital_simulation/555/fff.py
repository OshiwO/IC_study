'''
NORG(Input a, Input b)
'''
class NORG:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.Out = 1

    def run(self):
        if self.a == 0 and self.b == 0:
            self.Out = 1
        else:
            self.Out = 0


'''
RSLATCH(Input R, Input S)
'''
class RSLATCH:
    def __init__(self, R, S):
        self.R = R
        self.S = S
        self.Out = 0
        self.NOut = 0
        self.OutNext = NORG(R,self.NOut)
        self.NOutNext = NORG(self.Out,S)
    def run(self, qR, qS):
        self.OutNext.a = qR
        self.NOutNext.b = qS
        self.OutNext.run()
        self.NOutNext.run()
        self.Out = self.OutNext.Out
        self.NOut = self.NOutNext.Out
        self.OutNext.b = self.NOut
        self.NOutNext.a = self.Out


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

'''
THR is the threshold of upper comparator
TRI is the trigger of lower comparator
VH, VL are two inner value of 555 chip for normal case higher value equals to 2/3 vdd and lower
value equals to 1/3 vdd. But peopel could setting values by themselves.
DIS is the pin for discharging the voltage at threshold, it is a kind of sign which only has digital high or low
VDD is the power supply voltage
'''
### 定义555芯片内部
class nfff:
    def __init__(self,THR,TRI,VH,VL,DIS,VDD):
        self.THR = THR
        self.TRI = TRI
        if VH == 0 and VL == 0:
            self.VH = 2/3 * VDD
            self.VL = 1/3 * VDD
        else:   
            self.VH = VH
            self.VL = VL

        self.Vc1 = COMP(THR,self.VH)             ### 比较器1
        self.Vc2 = COMP(self.VL,TRI)             ### 比较器2 

        self.Vrs = RSLATCH(self.Vc1,self.Vc2)   ### 锁存器

        self.DIS = DIS
        self.Out = 0
    def run(self):                          ### 运行
        self.Vc1.a = self.THR
        self.Vc2.b = self.TRI
        self.Vc1.run()
        self.Vc2.run()
        self.Vrs.R = self.Vc1.Out
        self.Vrs.S = self.Vc2.Out
        self.Vrs.run(self.Vrs.R, self.Vrs.S)
        self.Out = self.Vrs.Out
        self.DIS = self.Vrs.NOut
        
