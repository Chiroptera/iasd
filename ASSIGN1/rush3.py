import rushDomain

def generalSearch(problem):

    frontier=list() # create list for states in frontier
    explored=list() # create list for explored states
    paths=list() # crate list for possible paths

    frontier.append(problem) # append original problem to frontier

    while 1:

        if len(frontier) == 0: # if frontier is empty, no solution found
            return False

        # decide which state from the fronter to explore (always the 1st)
        current_state=frontier.pop(0)

        # add state chosen to explored set
        explored.append(current_state)

        # determine actions available fo current state
        current_actions=rushDomain.actions(current_state)

        for x in current_actions: #for each action
            next_state=rushDomain.results(current_state,x) # determine its result

            if rushDomain.goaltest(next_state) is True: # if result is goal
                paths.append(rushDomain.buildPath(next_state)) # calculate path to result and add it to paths
                return paths                                   # return first solution found


            chkTemp=0
            for exp in explored:
                if rushDomain.cmpStates(next_state,exp):
                    chkTemp=-1
                    break
            if chkTemp is not -1:
                for fro in frontier:
                    if rushDomain.cmpStates(next_state,fro):
                        chkTemp=-1
                        break
            if chkTemp is 0:
                #frontier.insert(0,next_state) #depth search
                frontier.append(next_state) #breath first search
