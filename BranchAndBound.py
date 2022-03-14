from collections import namedtuple
from dataclasses import dataclass
from re import L
import sys
sys.setrecursionlimit(100000)

Item = namedtuple("Item", ['index', 'value', 'weight'])


@dataclass
class Solution:
    Items: list[int]
    value: int
    remainingCapacity: int


def sortItems(Items):
    sortedItems = list(filter(lambda x: x.value > 0, Items))
    return sorted(
        sortedItems, key=lambda x: float(x.weight)/float(x.value))


def getItemValuePerWeight(items):
    return list(
        map(lambda x: x.value/x.weight, items))


if __name__ == "__main__":
    filename = "data/ks_10000_0"
    Items = []

    with open(filename) as f:
        numItems, capacity = tuple(map(int, f.readline().strip().split(" ")))
        for itemIdx, line in enumerate(f.readlines()):
            value, weight = tuple(map(int, line.strip().split(" ")))
            Items.append(Item(itemIdx, value, weight))
    sortedItems = sortItems(Items)
    itemValuePerWeight = getItemValuePerWeight(sortedItems)
    global bestSolution
    bestSolution = Solution(value=0, Items=[], remainingCapacity=0)

    def getOptimisticSolutionValue(solution: Solution, itemIndex: int):
        return solution.value+solution.remainingCapacity*itemValuePerWeight[itemIndex]

    def branchAndBoundSolution(branchItemIndex: int = 0, branchSolution: Solution = Solution(Items=[], value=0, remainingCapacity=capacity)):
        global bestSolution
        if numItems == branchItemIndex:
            if (branchSolution.value > bestSolution.value):
                bestSolution = branchSolution
                print(bestSolution)
        else:
            branchItem = sortedItems[branchItemIndex]
            if getOptimisticSolutionValue(branchSolution, branchItemIndex) > bestSolution.value:
                remainingCapacityWithItem = branchSolution.remainingCapacity-branchItem.weight
                valueWithItem = branchSolution.value+branchItem.value
                if (remainingCapacityWithItem >= 0):
                    branchSolutionWith = Solution(
                        Items=[branchItem.index]+branchSolution.Items, remainingCapacity=remainingCapacityWithItem, value=valueWithItem)
                    branchAndBoundSolution(branchItemIndex +
                                           1, branchSolutionWith)
                branchAndBoundSolution(branchItemIndex +
                                       1, branchSolution=branchSolution)
    branchAndBoundSolution()
    print("Final Best Solution")
    print(bestSolution)
