import rushDomain

####################### Function #############################
#
# Name: generalSearch
# Input: state
# Output: solution
# Description:
#
#
#
#
#############################################################

def generalSearch(problem):

    frontier=list() # create list for states in frontier
    explored=list() # create list for explored states
    paths=list() # crate list for possible paths

    rushDomain.setHeuristic(problem,rushDomain.h(problem)) # set initial state heuristic value
    frontier.append(problem) # append original problem to frontier

    # statistics variable and list
    nodegen = 0
    branching = list()

    while 1:
        if len(frontier) == 0: # if frontier is empty, no solution found
            return False

        # get state with minimum heuristic
        current_state=rushDomain.hmin(frontier)

        # remove state chosen from frontier
        frontier.remove(current_state)

        # add state chosen to explored set
        explored.append(current_state)

        # determine actions available for current state
        current_actions=rushDomain.actions(current_state)

        localnode = 0

        for x in current_actions: #for each action
            next_state = rushDomain.results(current_state,x) # determine its result

            if rushDomain.goaltest(next_state) is True: # if result is goal
                # reconstruct solution path and add it to paths
                paths.append(rushDomain.buildPath(next_state))

                paths.append(nodegen)
		paths.append(sum(branching) / float(len(branching)))

                return paths    # return first solution found


            chkTemp = 0
            for exp in explored:
                # checks if new state belongs to explores and
                # if it does checks if its depth is bigger than the explored state
                # we don't want to add states with bigger depth to frontier
                if rushDomain.cmpStates(next_state,exp) and rushDomain.stateDepth(next_state) >= rushDomain.stateDepth(exp):
                    chkTemp = -1 # new states with bigger depth are not added
                    break

            if chkTemp is 0:
                for fro in frontier:
                    # checks if new state belongs to the frontier
                    if rushDomain.cmpStates(next_state,fro):
                        # if new state has less depth than state in frontier, then
                        # delete state in frontier because new state will be added after
                        # and is better than the previous
                        if rushDomain.stateDepth(next_state) < rushDomain.stateDepth(fro):
                            frontier.remove(fro)
                        else:
                            chkTemp = -1
                        break;

            # if new state doesn't belong to frontier or explored or has
            # a depth lower that any other state, add state to frontier
            if chkTemp is 0:
                nodegen=nodegen+1
                localnode=localnode+1
                rushDomain.setHeuristic(next_state,rushDomain.h(next_state)+rushDomain.stateDepth(next_state))
                frontier.append(next_state)
        branching.append(localnode)
