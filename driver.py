# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 06:46:12 2020

@author: Vipul
"""

import queue as Q

import time

#import resource

import sys

import math

from heapq import heappush,heappop,heapify

#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput(solstate):

    ### Student Code Goes here
    #print("Solution Found : ", solstate.config)
    
    print("cost_of_path : ", solstate.cost)
    print("max_search_depth : ", max_search_depth)
    print("search_depth : ", solstate.cost)
    #print("action : ", solstate.action)
    outf=open("output.txt","w")
    
    prnt=solstate.parent
    import psutil
    print("psutil", round(psutil.Process().memory_info().rss/(1024*1024),8))
    actionlist=[]
    actionlist.insert(0,solstate.action)
    #actionlist.insert(0,prnt.action)
    while prnt is not None:
        #print("parent : ", prnt.config)
        #print("Cost : ", prnt.cost)
        #print("action : ", prnt.action)
        if prnt.parent is not None:
           actionlist.insert(0,prnt.action)
        prnt=prnt.parent
       
    endt=time.time()
    print("Processing Time : ", round((endt-begt),8)," Seconds")
    print("Action: ", actionlist)
    outf.write("path_to_goal: "+ str(actionlist)+"\n")
    outf.write("cost_of_path: "+ str(solstate.cost)+"\n")
    outf.write("nodes_expanded: "+ str(expanded)+"\n")
    outf.write("search_depth: "+ str(solstate.cost)+"\n")
    outf.write("max_search_depth: "+ str(max_search_depth)+"\n")
    outf.write("running_time: "+ str(f'{round((endt-begt),8):.8f}')+"\n")
    outf.write("max_ram_usage: "+ str(f'{round(psutil.Process().memory_info().rss/(1024*1024),8):.8f}')+"\n")

def bfs_search(initial_state):

    """BFS search"""

    ### STUDENT CODE GOES HERE ###
    #global max_search_depth
    global max_search_depth,begt,expanded
    frontier=Q.Queue()
    frontier2=set()
    explored=set()
    expanded=0
    #frontier.put_nowait(initial_state.config)
    frontier.put_nowait(initial_state)
    #frontier2.append(initial_state.config)
    frontier2.add(initial_state.config)
    #state=(0,0,0,0,0,0,0,0,0)
    while not frontier.empty():
        state=frontier.get_nowait()
        explored.add(state.config)
        #print(state.config)
        
        if test_goal(state.config):
            print("Goal state Found")
            print("explored", len(explored))
            print("expanded", expanded)
            #break
            return state
        else:
            neighbors=state.expand()
            expanded=expanded+1
            
        #comb=frontier2+explored
        
        for neighbor in neighbors:
            #if neighbor.config not in comb:
            if neighbor.config not in frontier2 and neighbor.config not in explored:
                frontier.put_nowait(neighbor)
                frontier2.add(neighbor.config)
                if neighbor.cost>max_search_depth:
                    max_search_depth=neighbor.cost
    return None
        
        

def dfs_search(initial_state):

    """DFS search"""

    ### STUDENT CODE GOES HERE ###
    #global max_search_depth
    global max_search_depth,begt,expanded
    frontier=Q.LifoQueue()
    frontier2=set()
    explored=set()
    expanded=0
    
    #frontier.put_nowait(initial_state.config)
    frontier.put_nowait(initial_state)
    #frontier2.append(initial_state.config)
    frontier2.add(initial_state.config)
    #state=(0,0,0,0,0,0,0,0,0)
    while not frontier.empty():
        state=frontier.get_nowait()
        explored.add(state.config)
        #print(state.config)
        
        if test_goal(state.config):
            print("Goal state Found")
            print("explored", len(explored))
            print("expanded", expanded) #Expanded is 1 less than explored, because goal state is in explored, but it is not expanded.
            #break
            return state
        else:
            neighbors=state.expand()
            #print(neighbors)
            neighbors.reverse()
            expanded=expanded+1
            #print(neighbors)
            
        #comb=frontier2+explored
        
        for neighbor in neighbors:
            #if neighbor.config not in comb:
            if neighbor.config not in frontier2 and neighbor.config not in explored:
                frontier.put_nowait(neighbor)
                frontier2.add(neighbor.config)
                if neighbor.cost>max_search_depth:
                    max_search_depth=neighbor.cost
    return None

def A_star_search(initial_state):

    """A * search"""

    ### STUDENT CODE GOES HERE ###
    #global max_search_depth
    global max_search_depth,begt,expanded
    frontier=[]
    frontier2=set()
    explored=set()
    expanded=0
    counter=0
    #tst=[]
    #frontier.put_nowait(initial_state)
    costfn=calculate_total_cost(initial_state)
    heappush(frontier, tuple((costfn,counter,initial_state.config, initial_state)))
    frontier2.add(initial_state.config)
    
    while frontier:
        #print("Loop starts")
        #print(frontier)
        state=heappop(frontier)[3]
        #print(state)
        explored.add(state.config)
        #tst.append(state.action)
        #print("addes to exp")
        #print(state.config)
        
        if test_goal(state.config):
            print("Goal state Found")
            #print(tst)
            print("explored", len(explored))
            print("expanded", expanded)
            #break
            return state
        else:
            neighbors=state.expand()
            expanded=expanded+1
            #print("expanded")
            
        #comb=frontier2+explored
        
        for neighbor in neighbors:
            #if neighbor.config not in comb:
            #print(neighbor.config)
            if neighbor.config not in frontier2 and neighbor.config not in explored:
                #counter=counter+1
                if neighbor.action=="Up":
                    counter=1
                elif neighbor.action=="Down":
                    counter=2
                elif neighbor.action=="Left":
                    counter=3
                elif neighbor.action=="Right":
                    counter=4
                    
                #print(counter)
                costfn=calculate_total_cost(neighbor)
                #print("b4 push ", costfn, " ,", neighbor, " frontier: ", frontier)
                heappush(frontier, tuple((costfn,counter,neighbor.config, neighbor)))
                #print("aftr push",  frontier)
                #frontier.put_nowait(neighbor)
                #heapify(frontier)
                frontier2.add(neighbor.config)
                if neighbor.cost>max_search_depth:
                    max_search_depth=neighbor.cost
            elif neighbor.config in frontier2:
                for st in frontier:
                    if st[2]==neighbor.config:
                        costfn=calculate_total_cost(neighbor)
                        if st[0]>costfn:
                            #counter=counter+1
                            #print(st in frontier , " and " , len(frontier))
                            #frontier[int(frontier.index(st))]=tuple((costfn,0, neighbor,neighbor.config))
                            #frontier[int(frontier.index(st))]=tuple((costfn,0, st[2],st[3]))
                            frontier[int(frontier.index(st))]=tuple((costfn,st[1], st[2],st[3]))
                            #frontier[int(frontier.index(st))]=tuple((costfn,counter, st[2],st[3]))
                            #frontier[int(frontier.index(st))]=tuple((st[0],st[1], st[2],st[3]))
                            #print(frontier)
                            #print("====")
                            heapify(frontier)
                            
                            #print(neighbor.config, " ", costfn, " ", counter)
                            #print(st[3], " ", st[0], " ", st[1])
                            #print(st in frontier , " and " , len(frontier))
        #print("Loop ends")
    return None

def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###
    manh_d=calculate_manhattan_dist(state)
    costfn=manh_d+state.cost
    return costfn

#def calculate_manhattan_dist(idx, value, n):
def calculate_manhattan_dist(state):

    """calculate the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###
   
    #g=(0,1,2,3,4,5,6,7,8)
    #manh_d=sum(abs(x-y) for x,y in zip(state.config,g) if x !=0)
    """manh_d = 0
    for i,item in enumerate(state.config):
        prev_row,prev_col = int(i/ 3) , i % 3
        goal_row,goal_col = int(item /3),item % 3
        manh_d += abs(prev_row-goal_row) + abs(prev_col - goal_col)"""
    manh_d=sum( abs(x//3-i//3)+abs(x%3-i%3) for i,x in enumerate(state.config) if x!=0)
        
    return manh_d

def test_goal(puzzle_state):

    """test the state is the goal state or not"""

    ### STUDENT CODE GOES HERE ###
    goal_state=(0,1,2,3,4,5,6,7,8)
    return goal_state==puzzle_state

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

    global max_search_depth,begt,expanded
    max_search_depth=0
    #print("Starting !")
    #print(__name__)
    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)
    
    begt=time.time()

    if sm == "bfs":

        #print(hard_state.config)
        sol=bfs_search(hard_state)
        if sol is not None:
            print("Solution Found : ", sol.config)
            endt=time.time()
            print("Processing Time : ", round((endt-begt),8)," Seconds")
            writeOutput(sol)

    elif sm == "dfs":

        sol=dfs_search(hard_state)
        if sol is not None:
            print("Solution Found : ", sol.config)
            endt=time.time()
            print("Processing Time : ", round((endt-begt),8)," Seconds")
            writeOutput(sol)

    elif sm == "ast":

        sol=A_star_search(hard_state)
        if sol is not None:
            print("Solution Found : ", sol.config)
            endt=time.time()
            print("Processing Time : ", round((endt-begt),8)," Seconds")
            writeOutput(sol)

    else:

        print("Enter valid command arguments !")

if __name__ == '__main__':

    main()