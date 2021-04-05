import numpy as np

class Point(object):

    def __init__(self, id='', coord=np.array([[0.0],[0.0],[0.0]])):
        self.id = id
        self.coord = coord

    def __repr__(self):
        return self.coord.__repr__()
    def __str__(self):
        return self.coord.__str__()
