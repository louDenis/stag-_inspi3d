from vray import Renderer, AColor, Transform, Matrix, Vector


def intersect(a, b) :
    print(a.minimum, a.maximum)
    print(b.minimum, b.maximum)
    res= (a.minimum.x <= b.maximum.x and a.maximum.x >= b.minimum.x) and (a.minimum.y <= b.maximum.y and a.maximum.y >= b.minimum.y)
    print("res intersect=", res)
    return res

class aled:
    def __init__(self):
        self.minimum = None
        self.maximum = None
    def set_min_max(self,min,max):
        self.minimum = min
        self.maximum = max

a = aled()
a.set_min_max(Vector(0.0, 0.0,0.0), Vector(1.0, 1.0, 0.0))
b = aled()
b.set_min_max(Vector(0.0, 0.0, 0.0), Vector(3.0, 3.0, 0.0))
print("a.minimum.x=", a.minimum.x)
print("a.minimum.y=", a.minimum.y)
print("a.maximum.x=", a.maximum.x)
print("a.maximum.y=", a.maximum.y)
res = intersect(a, b)
