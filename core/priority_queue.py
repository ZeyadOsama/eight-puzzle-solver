import heapq

import utils.constants as c
from core.heuristics import init_heuristic


class PriorityQueue:
    def __init__(self, order=c.Order.MIN, heuristic=lambda x: x):
        self.__heap: heapq = []
        self.__heuristic = init_heuristic(order, heuristic)

    def append(self, item):
        """
        Insert item at its correct position.
        """
        heapq.heappush(self.__heap, (self.__heuristic(item), item))

    def pop(self):
        """
        Pop and return the item (with min or max f(x) value)
        depending on the order.
        """
        if self.__heap:
            return heapq.heappop(self.__heap)[1]
        raise Exception('Trying to pop from empty PriorityQueue.')

    def empty(self) -> bool:
        return self.__len__() == 0

    def __len__(self):
        """
        Return current capacity of PriorityQueue.
        """
        return len(self.__heap)

    def __contains__(self, key):
        """
        Return True if the key is in PriorityQueue.
        """
        return any([item == key for _, item in self.__heap])

    def __getitem__(self, key):
        """
        Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present.
        """
        for value, item in self.__heap:
            if item == key:
                return value
        raise KeyError(f'{str(key)} is not in the priority queue')

    def __delitem__(self, key):
        """
        Delete the first occurrence of key.
        """
        try:
            del self.__heap[[item == key for _, item in self.__heap].index(True)]
        except ValueError:
            raise KeyError(f'{str(key)} is not in the priority queue.')
        heapq.heapify(self.__heap)
