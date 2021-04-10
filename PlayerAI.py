# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 07:50:33 2020

@author: Vipul
"""

from random import randint

from BaseAI import BaseAI

#import Grid

import math
import time


class PlayerAI(BaseAI):

    def __init__(self):
        self.a=1
        self.depth=0
        self.prevTime = time.clock()
        self.limit=.047
        
        #self.weights=[[512,64,32,8],[256,16,8,4],[32,8,4,2],[8,4,2,0]]
        self.weights=[[2048, 1024, 64, 32],[512, 128, 16, 2],[256, 8, 2, 1],[4, 2, 1, 1]]
        
    def getMove(self, grid):
    
        #moves = grid.getAvailableMoves()
        
        #return moves[randint(0, len(moves) - 1)] if moves else None
        self.depth=0
        self.prevTime = time.clock()
        move,utility=self.maximise(grid,-math.inf ,math.inf )
        return move

    
    def maximise(self, grid,a,b):
        """global depth
        if not depth:
            depth=0"""
        self.depth+=1
        moves = grid.getAvailableMoves()
        #if not moves or self.depth>10: #terminal state
        if not moves or time.clock()-self.prevTime>self.limit:
            #print("Depth: ", self.depth)
            return None,self.evalstate(grid)
        
        maxMove, maxUtility= None, a
        
        for mv in moves:
            child=grid.clone()
            child.move(mv)
            step,utility=self.minimise(child,a,b)
            
            if utility>maxUtility:
                maxMove,maxUtility=mv,utility
                
            if maxUtility>=b:
                break
            if maxUtility>a:
                a=maxUtility
        
        return maxMove,maxUtility
        #return moves[randint(0, len(moves) - 1)] if moves else None
        
    def minimise(self, grid,a,b):

        moves = grid.getAvailableMoves()
        if not moves  or time.clock()-self.prevTime>self.limit: #terminal state
            return None,self.evalstate(grid)
        
        minMove, minUtility= None, b
        
        for mv in moves:
            child=grid.clone()
            child.move(mv)
            step,utility=self.maximise(child,a,b)
            
            if utility<minUtility:
                minMove,minUtility=mv,utility
                
            if minUtility<=a:
                break
            
            if minUtility<b:
                b=minUtility
        
        return minMove,minUtility
        
    def evalstate(self, state):
        #return max(max(state.map[0]),max(state.map[1]),max(state.map[2]),max(state.map[3]))
        h1_max=max(max(state.map[0]),max(state.map[1]),max(state.map[2]),max(state.map[3])) #Max tile value
        #if h1_max==state.map[0][0]:
        #if h1_max in [state.map[0][0],state.map[0][3],state.map[3][0],state.map[3][3]]:    
        if h1_max in [state.map[3][3]]:
            #h1_max_cor=2000
            h1_max_cor=math.log(h1_max)*10000
        else:
            h1_max_cor=-math.log(h1_max)*10000
        h2_avail=len(state.getAvailableCells()) #Total available cells
        #h3_sum=sum([sum(state.map[0]),sum(state.map[1]),sum(state.map[2]),sum(state.map[3])]) #Sum of tile value
        #h4_unq=len(set(state.map[0]+state.map[1]+state.map[2]+state.map[3]))
        h5_mono=self.monotonicity(state)
        
        
        #h6_pos_weight=sum(state.map[i][j]* self.weights[i][j] for i in range(4) for j in range(4) )
        
        h7_smooth=self.smooth(state)
        
        #h=h2_avail+(h1_max/2000)+(h3_sum/2000)
        #h=h2_avail-h4_unq/2
        #h=h2_avail+(h1_max/2048)+h5_mono*4#+h1_max_cor #This one gave 512 multiple times
        #h=h2_avail+h5_mono+h1_max_cor+h6_pos_weight
        #h=h2_avail+(h1_max/2048)+h5_mono*2-h7_smooth+h1_max_cor
        #h=h5_mono*2-h7_smooth # Think this gave the best results
        #h=h5_mono*4-h7_smooth*.5+h1_max_cor*1.2+(h2_avail)+h6_pos_weight
        #h=h5_mono*2-h7_smooth+h2_avail #This one worked  well too with old smoothness method
        h=h5_mono*4-h7_smooth+h2_avail+h1_max_cor
        return h
    
    """1def monotonicity(self, state):
        global monf
        monf0=0
        monf1=0
        for i in range(0,4):
            direction=state.map[i][0]-state.map[i][1]
            if direction<0:
                mon=-1
            else:
                mon=1
            #mon=1
            #mon=mon*direction
            for j in range(1,3):
                if (state.map[i][j]-state.map[i][j+1])*direction<0:
                    mon=0
                    break
            monf0=monf0+mon
        
        for j in range(0,4):
            direction=state.map[0][j]-state.map[1][j]
            if direction<0:
                mon=-1
            else:
                mon=1
            #mon=1
            #mon=mon*direction
            for i in range(1,3):
                if (state.map[i][j]-state.map[i+1][j])*direction<0:
                    mon=0
                    break
            monf1=monf1+mon
        monf=abs(monf0)+abs(monf1)
        #monf=(monf0)+(monf1)
        return monf"""
        
    """2def monotonicity(self, state):
        global monf
        monf0=0
        monf1=0
        for i in range(0,4):
            direction=state.map[i][0]-state.map[i][1]
            if direction<0:
                mon=-1
            else:
                mon=1
            #mon=1
            #mon=mon*direction
            for j in range(1,3):
                if (state.map[i][j]-state.map[i][j+1])*direction<0:
                    mon=0
                    break
            if mon<0:
                monf0=monf0+mon
            else:
                monf1=monf1+mon
        
        for j in range(0,4):
            direction=state.map[0][j]-state.map[1][j]
            if direction<0:
                mon=-1
            else:
                mon=1
            #mon=1
            #mon=mon*direction
            for i in range(1,3):
                if (state.map[i][j]-state.map[i+1][j])*direction<0:
                    mon=0
                    break
            #monf1=monf1+mon
            if mon<0:
                monf0=monf0+mon
            else:
                monf1=monf1+mon
        #monf=abs(monf0)+abs(monf1)
        #monf=(monf0)+(monf1)
        monf=max(abs(monf0),abs(monf1))
        return monf"""
        
    def monotonicity(self, state):
        global monf
        monf0=0
        monf1=0
        for i in range(0,4):
            if state.map[i][0]>=state.map[i][1] and state.map[i][1] >=state.map[i][2] and state.map[i][2] >=state.map[i][3]:
                mon=-1
            elif state.map[i][0]<=state.map[i][1] and state.map[i][1] <=state.map[i][2] and state.map[i][2] <=state.map[i][3]:
                mon=1
            else:
                mon=0
            
            #print(mon)
            if mon<0:
                monf0=monf0+mon
            else:
                monf1=monf1+mon
        
        for j in range(0,4):
            if state.map[0][j]>=state.map[1][j] and state.map[1][j] >=state.map[2][j] and state.map[2][j] >=state.map[3][j]:
                mon=-1
            elif state.map[0][j]<=state.map[1][j] and state.map[1][j] <=state.map[2][j] and state.map[2][j] <=state.map[3][j]:
                mon=1
            else:
                mon=0
            #print(mon)
            if mon<0:
                monf0=monf0+mon
            else:
                monf1=monf1+mon
        #monf=abs(monf0)+abs(monf1)
        #monf=(monf0)+(monf1)
        monf=max(abs(monf0),abs(monf1))
        return monf
                
    """def smooth(self, state):
        global smoothness
        smoothness=0
        for i in range(0,4):
            for j in range(0,3):
                smoothness=smoothness+abs(state.map[i][j]-state.map[i][j+1])
                smoothness=smoothness+abs(state.map[j][i]-state.map[j+1][i])
        return smoothness"""
                
    """def smooth(self, state):
        global smoothness
        smoothness=0
        for i in range(0,4):
            for j in range(0,3):
                smoothness=smoothness+abs(state.map[i][j]-state.map[i][j+1])
                smoothness=smoothness+abs(state.map[j][i]-state.map[j+1][i])
        return smoothness"""
    
    def smooth(self, state):
        global smoothness
        smoothness=0
        for i in range(0,3):
            for j in range(0,3):
                s1=abs(state.map[i][j]-state.map[i][j+1])
                s2=abs(state.map[i][j]-state.map[i+1][j])
                smoothness=smoothness+min(s1,s2)
                #smoothness=smoothness+abs(state.map[j][i]-state.map[j+1][i])
        return smoothness
    
    def mergeopp(self, state):
        global mergeop
        mergeop=0
        for i in range(0,4):
            for j in range(0,3):
                mergeop=mergeop+abs(state.map[i][j]-state.map[i][j+1])
                mergeop=mergeop+abs(state.map[j][i]-state.map[j+1][i])
        return mergeop
                
        