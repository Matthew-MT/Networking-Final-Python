import numpy

speed = 1

class Bullet:
  def __init__(self):
    self.position = (0, 0)
    self.slope = numpy.array([1, 0])
