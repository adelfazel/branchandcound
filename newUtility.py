import functools
import math
class solver():
    def __init__(self, Items, capacity):
        self.sortedItems = list(filter(lambda x: x.value > 0, Items))
        self.sortedItems = sorted(self.sortedItems, key=lambda x:float(x.weight)/float(x.value))
        self.ItemValuePerWeight = list(map(lambda x: x.value/x.weight,self.sortedItems))
        self.numItems = len(self.sortedItems)
        self.capacity = capacity
        self.bestSolution = solution(0, self.capacity)
        self.SolQueye = [(solution(0, self.capacity),0)]

    def isOptimisitcBetter(self, sol, newItemIdx):
        ItemValuePerWeight = self.ItemValuePerWeight[newItemIdx]
        rhs = sol.value + (sol.capacity*ItemValuePerWeight)
        return ( 0.95*rhs > self.bestSolution.value )

    def explore(self):
        if self.SolQueye:
            sol, itemIndex  = self.SolQueye.pop()
            if itemIndex < self.numItems:
                if self.isOptimisitcBetter(sol, itemIndex):
                    self.exploreLeft(sol, itemIndex)
                    self.exploreRight(sol, itemIndex)
            return True
        else:
            return False

    def exploreLeft(self, sol, itemIndex):
        newItem = self.sortedItems[itemIndex]
        thisSol = sol.copy()
        if thisSol.addItem(newItem):
            if thisSol.value > self.bestSolution.value:
                self.bestSolution = thisSol
            self.SolQueye.append((thisSol, itemIndex+1))

    def exploreRight(self, sol, itemIndex):
        if itemIndex+1<self.numItems:
            if self.isOptimisitcBetter(sol, itemIndex+1):
                self.SolQueye.append((sol, itemIndex+1))

    def solveWrapper(self):
        while self.explore():
             pass
             # self.SolQueye  = list(filter(self.isOptimisitcBetter(sol, itemIndex) self.SolQueye ,:


class solution():
    def __init__(self, value, capacity, items=set()):
        self.value, self.capacity = value, capacity
        self.items = items.copy()

    def copy(self):
        return solution(self.value,  self.capacity, self.items)

    def addItem(self, newItem):
        remainingCap = self.capacity-newItem.weight
        if remainingCap < 0:
            return False
        self.items.add(newItem)
        self.capacity = remainingCap
        self.value+=newItem.value
        return True
