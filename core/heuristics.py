import math

from core.common import Point
from utils.constants import Order


def manhattan(start_point: Point, end_point: Point) -> float:
    return abs(start_point.x - end_point.x) + abs(start_point.y - end_point.y)


def euclidean(start_point: Point, end_point: Point) -> float:
    return math.sqrt(math.pow(start_point.x - end_point.x, 2)
                     + math.pow(start_point.y - end_point.y, 2))


def init_heuristic(order, heuristic) -> lambda x: x:
    """
    Items are popped according to order.
    Order: Min -> Item with min f(x) will be popped first.
    Order: Max -> Item with max f(x) will be popped first
    """
    if order == Order.MIN:
        return heuristic
    elif order == Order.MAX:
        return lambda x: -heuristic(x)
    else:
        raise ValueError(f'Order must be either {Order.MIN} or {Order.MAX}.')
