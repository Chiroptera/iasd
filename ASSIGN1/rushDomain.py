import copy
import time
from operator import itemgetter

# aid variables -> help in referencing different things throughout the code
start=0 # references the coordinate of the beggining of the car
end=-1 # references the coordinate of the end of the car
lin=0 # references the line in which a position of a car is
col=1 # references the column in which a position of a car is

####################### Function #############################
#
# Name: printState
# Input: state, size of problem
# Output:
# Description: converts state to a matrix form, prints each
#              line of matrix as matrix to screen
#
#
#
#############################################################

def printState(stateIn):
    state = stateIn[-1]
    problemSize = stateIn[3]
    blank_matrix = [0]*problemSize[lin]

    for index,value in enumerate(blank_matrix):
        blank_matrix[index] = [0] * problemSize[col]

    for elem in state:
        for mat_lin,mat_col in state[elem]:
            blank_matrix[mat_lin][mat_col] = elem

    for print_state_line in blank_matrix:
        print "".join(print_state_line)

####################### Function #############################
#
# Name: loadProbem
# Input: filename (string)
# Output: state representation
# Description: reads problem from file, converts problem to
#              a dictionary and returns a list containing
#              all the parameters a state has: parent state (0),
#              action that resulted in current state (0),
#              heuristic value, problem size and board distribution
#
#############################################################

def loadProblem(filename):

    matrix = [line.strip() for line in open(filename)] #get all lines from file
    matrix = [line for line in matrix if line] #delete blank lines
    matrix = map(list,matrix) #seperate characters in string
    problemSize=[len(matrix),len(matrix[0])]
    problem=dict()

    # store agents in matrix to dictionary problems
    for line_num,line in enumerate(matrix): #for each line in matrix
        for elem_num,elem in enumerate(line): #for each element elem in line
            if elem not in problem:
                problem[elem]=[[line_num,elem_num]]
            else:
                problem[elem].append([line_num,elem_num])

    # [parent state,action,heuristic value,problem size,state]
    return [0,0,0,problemSize,problem]

def saveSolution(actionPath):
    pass

####################### Function #############################
#
# Name: actions
# Input: state (matrix of problem)
# Output: possible_actions (list of possible actions)
# Description: reads position of each car into dictionary; for
#              each car, check if movement is horizontal or
#              vertical; check how many moves possible for any
#              direction; return list of possible moves
#
#############################################################


def actions(stateIn):

    possible_actions=list()
    problemSize=stateIn[3]
    state=stateIn[-1]

    #for each car in the list, check what are the possible actions
    for car in state:
        if car is '-':
            continue

        ### HORIZONTAL MOVEMENT
        if state[car][start][lin] is state[car][end][lin]: #checks if the line of start and end coordinate match
            car_line=state[car][start][lin] #line in which car moves
            car_start_col=state[car][start][col] #head coordinate of car
            car_end_col=state[car][end][col] #tail coordinate of car

            ## check leftward movement
            if car_start_col is not 0: #if car doens't start at left wall
                move=1 #initiate move counter

                while True:
                    # if point before head is in the set of coordinates of '-', it's a possible move
                    if [car_line,car_start_col - move] in state['-']:
                        possible_actions.append([car,'L',move])
                        move = move +1
                    else:
                        break

            ## check rightward movement
            if car_end_col is not problemSize[col]-1:
                move=1

                while True:
                    if [car_line,car_end_col + move] in state['-']:
                        possible_actions.append([car,'R',move])
                        move = move +1
                    else:
                        break

    ### VERTICAL MOVEMENT
        elif state[car][start][col] is state[car][end][col]:
            car_col=state[car][start][col]
            car_start_lin=state[car][start][lin]
            car_end_lin=state[car][end][lin]

            ## check upward movement
            if car_start_lin is not 0: #if car doesn't start at upper wall
                move=1

                while True:
                    # if point before head is in the set of coordinates of '-', it's a possible move
                    if [car_start_lin - move,car_col] in state['-']:
                        possible_actions.append([car,'U',move])
                        move = move +1
                    else:
                        break

            ##check downward movement
            if state[car][end][lin] is not problemSize[lin]-1: #if state doesn't end at lower wall
                move=1
                while True:
                    # if point before head is in the set of coordinates of '-', it's a possible move
                    if [car_end_lin + move,car_col] in state['-']:
                        possible_actions.append([car,'D',move])
                        move = move +1
                    else:
                        break
    return possible_actions


####################### Function #############################
#
# Name: results
# Input: state, action <- [car,direction,quantity]
# Output: result_state
# Description: reads position of each car into dictionary; for
#              each car, check if movement is horizontal or
#              vertical; check how many moves possible for any
#              direction; return list of possible moves
#
#############################################################

def results(state,action):
    result_state=copy.deepcopy(state[-1])

    ## MOVE LEFT
    if action[1] is 'L':
        for x in range(action[2]):
            for ind,coord in enumerate(result_state[action[0]]):
                 if ind == len(result_state[action[0]])-1:
                    result_state['-'].append(coord[:])
                 coord[col]=coord[col]-1
                 if ind == 0:
                     result_state['-'].remove(coord)

    ## MOVE RIGHT
    elif action[1] is 'R':
        for x in range(action[2]):
            for ind,coord in enumerate(result_state[action[0]]):
                if ind == 0:
                    result_state['-'].append(coord[:])
                coord[col]=coord[col]+1
                if ind == len(result_state[action[0]])-1:
                    result_state['-'].remove(coord)
    ## MOVE UP
    elif action[1] is 'U':
        for x in range(action[2]):
            for ind,coord in enumerate(result_state[action[0]]):
                if ind == len(result_state[action[0]])-1:
                    result_state['-'].append(coord[:])
                coord[lin]=coord[lin]-1
                if ind == 0:
                    result_state['-'].remove(coord)
    ## MOVE DOWN
    elif action[1] is 'D':
        for x in range(action[2]):
            for ind,coord in enumerate(result_state[action[0]]):
                if ind == 0:
                    result_state['-'].append(coord[:])
                coord[lin]=coord[lin]+1
                if ind == len(result_state[action[0]])-1:
                    result_state['-'].remove(coord)

    result_state['-'].sort() # this has to be done to ensure correct state comparison in general search
    problemSize=state[3]     # problem size must be in result state

    return [state,list(action),0,problemSize,result_state]


####################### Function #############################
#
# Name: goaltest
# Input: state, problemSize
# Output: boolean
# Description: checks if end of the car is right wall of board
#
#############################################################

def goaltest (state):
    problemSize=state[3]

    # last column of red car must equal last column of problem
    if state[-1]['R'][end][col] == problemSize[col]-1 :
        return True
    return False

####################### Function #############################
#
# Name: pathCost
# Input: path
# Output: length of path
# Description:
#
#
#
#
#############################################################

def pathCost(path):
    cost=0
    for x in path:
        cost = cost + x[2]
    return cost



####################### Function #############################
#
# Name: stateDepth
# Input: state
# Output: depth of state
# Description: builds the path from current state to initial
#              problem and calculates it's length.
#
#############################################################

def stateDepth(state):
    #return pathCost(buildPath(state)) # return real path cost
    return len(buildPath(state)) #return depth level

####################### Function #############################
#
# Name: cmpStates
# Input: state1, state2
# Output: True or False
# Description: takes two states and compares if their boards
#              are equal (True) or not (False)
#
#############################################################

def cmpStates(state1,state2):
    if state1[-1] == state2[-1]:
        return True
    else:
        return False

####################### Function #############################
#
# Name: buildPath
# Input: state
# Output: path
# Description: receives a state and tracks the previous states
#              until the very first or
#
#############################################################

def buildPath(state):
    solution=list()
    while(state[0] is not 0):   # while initial state is not reached
        solution.insert(0,state[1]) # add state state to solution path
        state=state[0]              # state is now its parent
    return solution


     ############################################################
     #                                                          #
     #            HEURISTIC                                     #
     #                                                          #
     #                      RELATED                             #
     #                                                          #
     #                                  FUNCTIONS               #
     #                                                          #
     ############################################################

####################### Function #############################
#
# Name: h
# Input: state, problem size
# Output: hValue
# Description: receives a state and computes the heuristic
#              value for that state
#
#############################################################

def h(state):
    board=state[-1]           # get board from state
    problemSize=state[3]      # get problem size from state representation
    Rcol=board['R'][end][col] # get column of red car
    Rlin=board['R'][end][lin] # get line of red car

    # compute direct path to goal
    directPath = 0
    directPath = problemSize[col] - 1 - Rcol

    # compute number of obstacles (cars) between red car and goal
    numObstacles = 0
    for x in range(Rcol+1,problemSize[col]):
        if [Rlin,x] not in board['-']:
            numObstacles = numObstacles + 1

    # store heuristic in state
    #numObstacles = 0 # simple direct path heuristic
    directPath = 0 # simple number of obstacles heuristic
    return directPath+numObstacles


####################### Function #############################
#
# Name: decide
# Input: frontier
# Output: state
# Description: receives frontier and returns the state with
#              the minimum heuristic value
#
#############################################################

def setHeuristic(state,heuristic):
    state[2] = heuristic


####################### Function #############################
#
# Name: hmin
# Input: frontier
# Output: state
# Description: receives frontier and returns the state with
#              the minimum heuristic value
#
#############################################################

def hmin (frontier):
    return min(frontier, key=itemgetter(2))

####################### Function #############################
#
# Name: chkTriangle
# Input: stateP (parent), stateC (child)
# Output: True or False
# Description: check triangle inequality
#
#
#############################################################

def chkTriangle (stateP,stateC):
    if stateP[2] <= stateC[1][-1] + h(stateC):
        return True
    return False
