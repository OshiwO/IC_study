## 这里进行简单锁存器的模拟


##
class NORG:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.Out = 1

    def run(self):
        if self.a == 1 and self.b == 1:
            self.Out = 1
        else:
            self.Out = 0



class RSLATCH:
    def __init__(self, R, S):
        self.R = R
        self.S = S
        self.Out = 0
        self.NOut = 1
        self.OutNext = NORG(R,self.NOut)
        self.NOutNext = NORG(S,self.Out)
    def run(self):
        self.OutNext.run()
        self.NOutNext.run()
        self.Out = self.OutNext.Out
        self.NOut = self.NOutNext.Out

