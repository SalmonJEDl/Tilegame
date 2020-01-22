from queue import PriorityQueue
import math
from gui import *


"""
value = current state of the board
parent = parent
start = start
goal = tile list of a completed game
"""
class State(object):
    def __init__(self, value, parent, start = None, goal = None):
        self.children = []
        self.parent = parent
        self.value = value
        self.current_row = 0
        self. width = int(math.sqrt(len(value)))
        if parent:
            self.path = parent.path.copy()

            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = []
            self.start = start
            self.goal = goal
        
        self.dist = self.getDist()
            
            
    def getDist(self):
        boardgrid = self.gridify(self.value)
        goalgrid = self.gridify(self.goal)
        if self.value == self.goal:
            return 0
        distance = 0
        
        for k in range(0, self.width-2):
            if boardgrid[k] == goalgrid[k]:
                self.current_row += 1
            else:
                break
        
        for i in range(0, self.width):
            for j in range(self.current_row, self.width):
                try:
                    x = boardgrid[j].index(goalgrid[self.current_row][i])
                except:
                    continue
                distance += abs(self.current_row - j) + abs(i - x)
        
        """for i in range(0,self.width):
            for j in range(0, self.width):
                boardgrid.index()
                if goalgrid[y][x] == boardgrid[i][j]
                tile = self.goal[i]
                distance += abs(i-self.value.index(tile))"""
                
        return distance
            
            
    def gridify(self, text):
        grid = []
        for i in range(0, self.width):
            grid.append(text[i*self.width:(i+1)*self.width])
        return grid        
        
        
    def createChildren(self):
        empty_loc = self.value.index("*")
        
        def swap_tiles(first, second):
            newlist = self.value.copy()
            temp = newlist[first]
            newlist[first] = newlist[second]
            newlist[second] = temp
            return newlist
        
            def in_empty_row(num):
                return num < (self.current_row* self.width)
            
        if empty_loc >= self.width:
            child = State(swap_tiles(empty_loc, empty_loc - self.width), self)
            child.path.append(empty_loc - self.width)
            self.children.append(child)
        if empty_loc < len(self.value) - self.width:
            child = State(swap_tiles(empty_loc, empty_loc + self.width), self)
            child.path.append(empty_loc + self.width)
            self.children.append(child)
        if empty_loc % self.width != 0:
            child = State(swap_tiles(empty_loc, empty_loc - 1), self)
            child.path.append(empty_loc - 1)
            self.children.append(child)
        if (empty_loc+1) % self.width != 0:
            child = State(swap_tiles(empty_loc, empty_loc + 1), self)
            child.path.append(empty_loc + 1)
            self.children.append(child)
            
        

class AStar():
    def __init__(self, start, goal):
        self.path = []
        self.visited =[]
        self.queue = PriorityQueue()
        self.start = start
        self.goal = goal
        
    def solve(self):
        beginState = State(self.start, None, self.start, self.goal)
        
        count = 0
        self.queue.put((0, count, beginState))
        while (not self.path and self.queue.qsize):
            closest = self.queue.get()[2]
            closest.createChildren()
            self.visited.append(closest.value)
            for child in closest.children:
                if child.value not in self.visited:
                    count +=1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.queue.put((child.dist, count, child))
        return self.path
    
    
    
if __name__ == "__main__":
    tiles = Tiles(3)
    tiles.shuffle(50)
    print(tiles)
    a = AStar(tiles.shufflelist, tiles.tilelist)
    a.solve()
    print(a.path)
    