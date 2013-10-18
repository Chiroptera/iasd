import copy
import time

# aid variables -> help in referencing different things throughout the code
start=0 # references the coordinate of the beggining of the car
end=-1 # references the coordinate of the end of the car
lin=0 # references the line in which a position of a car is
col=1 # references the column in which a position of a car is

####################### Function #############################
#
# Name: printState
# Input: state, size of problem
# Output: nothin
# Description: converts state to a matrix form, prints each
#              line of matrix as matrix to screen
#              
#              
#
#############################################################

def printState(state,problemSize):
    blank_matrix=[0]*problemSize[lin]
    for index,value in enumerate(blank_matrix):
        blank_matrix[index]=[0]*problemSize[col]
    for elem in state:
        for mat_lin,mat_col in state[elem]:
            blank_matrix[mat_lin][mat_col]=elem
    for print_state_line in blank_matrix:
        print "".join(print_state_line)

####################### Function #############################
#
# Name: loadProbem
# Input: filename (string)
# Output: list with problem and problem sie
# Description: 
#              
#              
#              
#
#############################################################

def loadProblem(filename):
    
    matrix = [line.strip() for line in open(filename)] #get all lines from file
    matrix = [line for line in matrix if line] #delete blank lines
    matrix = map(list,matrix) #seperate characters in string
    problemSize=[len(matrix),len(matrix[0])]
    problem=dict()
    # store agens in matrix to dictionary problems
    for line_num,line in enumerate(matrix): #for each line in matrix
        for elem_num,elem in enumerate(line): #for each element elem in line
            if elem not in problem:
                problem[elem]=[[line_num,elem_num]]
            else:
                problem[elem].append([line_num,elem_num])

    return [[0,0,0,problem],problemSize]

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


def actions(stateIn,problemSize):

    possible_actions=list()
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
    #print "list(action)=",action
    #print "return=",[state,list(action),result_state]
    #raw_input("wh")
    return [state,list(action),0,result_state]


####################### Function #############################
#
# Name: goaltest
# Input: state, problemSize
# Output: boolean
# Description: checks if end of the car is right wall of board
#
#############################################################

def goaltest (state,problemSize):
    if state[-1]['R'][end][col] == problemSize[col]-1 :
        return True
    return False

####################### Function #############################
#
# Name: path_cost
# Input: state (matrix of problem)
# Output: possible_actions (list of possible actions)
# Description: reads position of each car into dictionary; for
#              each car, check if movement is horizontal or
#              vertical; check how many moves possible for any
#              direction; return list of possible moves
#
#############################################################

def path_cost(path):
    return len(path)
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
    while(state[0] is not 0):
        # print "solution",solution
        # raw_input("get state[-1]")
        # print "state[1]",state[1]
        # raw_input("get state[1]")
        # print "state[1]",state[1]
        # raw_input("get state[0]")
        # print state[0]
#        raw_input("what")
        solution.insert(0,state[1])
        state=state[0]
    return solution
