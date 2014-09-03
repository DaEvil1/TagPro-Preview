#DK v. 2
from random import randint

class Point:

    def __init__(self, **options):
        self.data = {"position" : [0, 0], "velocity" : [0, 0],
                     "acceleration" : [0, 0], "height" : 0,
                     "width" : 0, "borders" : None, "friction" : [0, 0]}

        for element in options:
            self.data[element] = options[element]

    def Get(self, option):
        return self.data[option]

    def Move(self):
        for i in range(len(self.data["velocity"])):
            self.data["velocity"][i] += self.data["acceleration"][i]
            if self.data["velocity"][i] > 0:
                self.data["velocity"][i] += -self.data["friction"][i]
                if self.data["velocity"][i] < 0:
                    self.data["velocity"][i] = 0
            elif self.data["velocity"][i] < 0:
                self.data["velocity"][i] += +self.data["friction"][i]
                if self.data["velocity"][i] > 0:
                    self.data["velocity"][i] = 0                
            self.data["position"][i] += self.data["velocity"][i]

    def Modify(self, option, value):
        self.data[option] = value

    def RandInit(self, MaxV):
        self.data["Maxvel"] = MaxV

    def InsideX(self):
        maxX = self.data["position"][0] + self.data["width"]/2.0
        minX = self.data["position"][0] - self.data["width"]/2.0
        if maxX > self.data["borders"][2]:
            return "Max"
        if minX < self.data["borders"][0]:
            return "Min"
        return "Inside"

    def InsideY(self):
        maxY = self.data["position"][1] + self.data["height"]/2.0
        minY = self.data["position"][1] - self.data["height"]/2.0
        if maxY > self.data["borders"][3]:
            return "Max"
        if minY < self.data["borders"][1]:
            return "Min"
        return "Inside"

    def WallFix(self):
        acc = self.data["acceleration"]
        vel = self.data["velocity"]
        pos = self.data["position"]
        bor = self.data["borders"]
        widhei = self.data["width"], self.data["height"]
        inside = [self.InsideX(), self.InsideY()]
        for i in range(len(inside)):
            if inside[i] == "Max":
                self.data["position"][i] = bor[i + 2] - widhei[i] / 2.0 - 1
                self.data["velocity"][i] = 0
            elif inside[i] =="Min":
                self.data["position"][i] = bor[0] + widhei[i] / 2.0 + 1
                self.data["velocity"][i] = 0

    def RandMove(self):
        acc, vel = self.data["acceleration"], self.data["velocity"]
        pos, bor = self.data["position"], self.data["borders"]
        widhei = self.data["width"], self.data["height"]
        #rand = randint(-100000, 100000)
        #if rand == 0:
        #    rand = 1
        #rand2 = abs(100000 - rand)/20
        #a = rand/abs(rand)
        #x = rand % self.data["Maxvel"][0]*a
        #y = rand2 % self.data["Maxvel"][1]*a
        x = randint(- self.data["Maxvel"][0], self.data["Maxvel"][0])
        y = randint(- self.data["Maxvel"][1], self.data["Maxvel"][1])
        ints = [x, y]
        inside = [self.InsideX(), self.InsideY()]
        for i in range(len(inside)):
            if inside[i] == "Inside":
                if ints[i] > vel[i]:
                    acc[i] = abs(acc[i])
                elif ints[i] < vel[i]:
                    acc[i] = -abs(acc[i])
            else:
                if inside[i] == "Max":
                    pos[i] = bor[i + 2] - widhei[i] / 2.0
                    vel[i] = -vel[0]
                else:
                    pos[i] = bor[i] + widhei[i] / 2.0 
                    vel[i] = -vel[0]
        self.Move()


        
        
