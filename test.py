class test:
    def __init__(self, beep_obj):
        self.beep = beep_obj

    def name(self):
        print(self.beep.name)


class beep:
    def __init__(self, yarp):
        self.name = "zoop"
        self.num = 10
        self.yarp = yarp(self)

if __name__ == "__main__":

    boop = beep(test)

    boop.yarp.name()

    boop.name = "zoinks"
    
    boop.yarp.name()