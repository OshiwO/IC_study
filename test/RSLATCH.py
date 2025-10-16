## 这里进行简单锁存器的模拟


##
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

