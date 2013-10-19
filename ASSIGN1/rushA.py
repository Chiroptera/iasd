import copy
import time
from operator import itemgetter
import rushDomain

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

####################### Function #############################
#
# Name: saveSolution
# Input: path of actions
# Output: file with solution
# Description:
#
#
#
#
#############################################################

def saveSolution(actionPath):
    pass

####################### Function #############################
#
# Name: actions

####################### Function #############################
#
# Name: general_search
# Input: state
# Output: solution
# Description:
#
#
#
#
#############################################################

def generalSearch(problem,problemSize):

    frontier=list() # create list for states in frontier
    explored=list() # create list for explored states
    paths=list() # crate list for possible paths

    frontier.append(problem) # append original problem to frontier

    while 1:
        if len(frontier) == 0: # if frontier is empty, no solution found
            return False

        # take state with lowest estimation
        #current_state = frontier.pop(0)
        current_state=decide(frontier)
        frontier.remove(current_state)

        #somethin=itemgetter(2)
        #frontier_h=map(somethin,frontier)
        #("h of frontier sorted= "+str(frontier_h))

        #rushDomain.printState(current_state,problemSize)
        #print("current state evaluation="+str(current_state[2])+"\n\n")
        #raw_input("continue")

        # add state chosen to explored set
        explored.append(current_state)

        # determine actions available for current state
        current_actions=rushDomain.actions(current_state,problemSize)

        for x in current_actions: #for each action
            next_state = rushDomain.results(current_state,x) # determine its result

            if rushDomain.goaltest(next_state,problemSize) is True: # if result is goal
                 # reconstruct solution path and add it to paths
                paths.append(rushDomain.buildPath(next_state))
                return paths


            chkTemp = 0
            for exp in explored:
                # checks if new state belongs to explores and
                # if it does checks if its depth is bigger than the explored state
                # we don't want to add states with bigger depth to frontier
                if next_state[-1] == exp[-1] and rushDomain.stateDepth(next_state) >= rushDomain.stateDepth(exp):
                    chkTemp = -1 # new states with bigger depth are not added
                    break

            if chkTemp is not -1:
                for fro in frontier:
                    # checks if new state belongs to the frontier
                    if next_state[-1] == fro[-1]:
                        # if new state has less depth than state in frontier, then
                        # delete state in frontier because new state will be added after
                        if rushDomain.stateDepth(next_state) < rushDomain.stateDepth(fro):
                            frontier.remove(fro)
                        chkTemp = -1
                        break;

            # if new state doesn't belong to frontier or explored or has
            # a depth lower that any
            if chkTemp is 0:
                next_state[2]=rushDomain.h(next_state,problemSize) #+ rushDomain.stateDepth(next_state)
                # printState(next_state,problemSize)
                # print("next state evaluation="+str(next_state[2])+"\n\n")
                # raw_input("continue")
                frontier.append(next_state)

        # sort frontier's states by estimation value min to max
        # getcount=itemgetter(2)
        # thingy=map(getcount,frontier)

        # print("before="+str(thingy))
        # #sorted(frontier, key=getcount)
        # #frontier.sort()
        # getcount=itemgetter(2)
        # thingy=map(getcount,frontier)
        # print("after="+str(thingy))

        # minstate=decide(frontier)
        # rushDomain.printState(minstate,problemSize)
        # print("h of minstate="+str(minstate[2]))






####################### Function #############################
#
# Name: decide
# Input: frontier
# Output: state
# Description: receives frontier and returns the state with
#              the minimum heuristic value
#
#############################################################

def decide (frontier):
    return min(frontier, key=itemgetter(2))
