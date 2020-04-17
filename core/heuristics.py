import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def display(self):
        print(f'x: {self.x}')
        print(f'y: {self.y}')


def manhattan(start_point: Point, end_point: Point) -> float:
    return abs(start_point.x - end_point.x) + abs(start_point.y - end_point.y)


def euclidean(start_point: Point, end_point: Point) -> float:
    return math.sqrt(math.pow(start_point.x - end_point.x, 2)
                     + math.pow(start_point.y - end_point.y, 2))
