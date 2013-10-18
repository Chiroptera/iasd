import copy
import time

# aid variables -> help in referencing different things throughout the code
start=0 # references the coordinate of the beggining of the car
end=-1 # references the coordinate of the end of the car
lin=0 # references the line in which a position of a car is
col=1 # references the column in which a position of a car is

def printState(state,problemSize):
    blank_matrix=[0]*problemSize[lin]
    for index,value in enumerate(blank_matrix):
        blank_matrix[index]=[0]*problemSize[col]
    for elem in state:
        for mat_lin,mat_col in state[elem]:
            blank_matrix[mat_lin][mat_col]=elem
    for print_state_line in blank_matrix:
        print "".join(print_state_line)

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

    return [[0,0,problem],problemSize]

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
    return [state,list(action),result_state]


####################### Function #############################
#
# Name: goaltest
# Input: state, action
# Output: state
# Description: reads position of each car into dictionary; for
#              each car, check if movement is horizontal or
#              vertical; check how many moves possible for any
#              direction; return list of possible moves
#
#############################################################
def goaltest (state):
    if state[-1]['R'][end][col] == 5 :
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

def path_cost():
    pass

####################### Function #############################
#
# Name: general_search
# Input: state
# Output: possible_solutions
# Description: reads position of each car into dictionary; for
#              each car, check if movement is horizontal or
#              vertical; check how many moves possible for any
#              direction; return list of possible moves
#
#############################################################

def generalSearch(problem,problemSize):

    frontier=list() # create list for states in frontier
    explored=list() # create list for explored states
    paths=list() # crate list for possible paths

    frontier.append(problem) # append original problem to frontier

    while 1:
        #print "frontier len=",len(frontier)
        if len(frontier) == 0: # if frontier is empty, no solution found
            #print "num of paths=",len(paths)
            return paths

        current_state=frontier.pop(0)  # decide which state from the fronter to explore (always the 1st)

        #print("Tree level="+str(len(buildPath(current_state))))
#        print("Action choosen="+str(current_state[1]))


        explored.append(current_state) # add state chosen to explored set
        #printState(current_state[-1],problemSize)
        current_actions=actions(current_state,problemSize) # determine actions available fo current state

#        print("Possible actions for this state="+str(current_actions))
#        raw_input("continue")

        for x in current_actions: #for each action
            next_state=results(current_state,x) # determine its result

            if goaltest(next_state) is True: # if result is goal
                paths.append(buildPath(next_state)) # calculate path to result and add it to paths
                #print(str(paths[-1]))
                if len(paths[-1]) <= 87:
                    return paths
                #raw_input("sol found")
                #print "path len=",len(paths[-1])
                #return paths
                #raw_input("Solution found.")
                break #since current state leads to solution, ignore any other possible 

            chkTemp=0
            for exp in explored:
                if next_state[-1] == exp[-1]:
                    #printState(exp[-1],problemSize)
                    #print next_state
                    #printState(next_state[-1],problemSize)
                    #raw_input("continue...")
                    chkTemp=-1
                    break
            if chkTemp is not -1:
                for fro in frontier:
                    if next_state[-1] == fro[-1]:
                        chkTemp=-1
                        break
            if chkTemp is 0:
                #frontier.insert(0,next_state) #depth search
                frontier.append(next_state) #breath first search


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
