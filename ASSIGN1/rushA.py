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

    frontier.append(problem) # append original problem to frontier

    while 1:
        if len(frontier) == 0: # if frontier is empty, no solution found
            return False

        # get state with minimum heuristic
        current_state=rushDomain.hmin(frontier)

        # remove state chosen from frontier
        frontier.remove(current_state)

        #somethin=itemgetter(2)
        #frontier_h=map(somethin,frontier)
        #("h of frontier sorted= "+str(frontier_h))

        #rushDomain.printState(current_state)
        #print("current state evaluation="+str(current_state[2])+"\n\n")
        #raw_input("continue")

        # add state chosen to explored set
        explored.append(current_state)

        # determine actions available for current state
        current_actions=rushDomain.actions(current_state)

        for x in current_actions: #for each action
            next_state = rushDomain.results(current_state,x) # determine its result

            if rushDomain.goaltest(next_state) is True: # if result is goal
                 # reconstruct solution path and add it to paths
                paths.append(rushDomain.buildPath(next_state))
                return paths


            chkTemp = 0
            for exp in explored:
                # checks if new state belongs to explores and
                # if it does checks if its depth is bigger than the explored state
                # we don't want to add states with bigger depth to frontier
                if rushDomain.cmpStates(next_state,exp) and rushDomain.stateDepth(next_state) >= rushDomain.stateDepth(exp):
                    chkTemp = -1 # new states with bigger depth are not added
                    break

            if chkTemp is not -1:
                for fro in frontier:
                    # checks if new state belongs to the frontier
                    if rushDomain.cmpStates(next_state,fro):
                        # if new state has less depth than state in frontier, then
                        # delete state in frontier because new state will be added after
                        if rushDomain.stateDepth(next_state) < rushDomain.stateDepth(fro):
                            frontier.remove(fro)
                        chkTemp = -1
                        break;

            # if new state doesn't belong to frontier or explored or has
            # a depth lower that any
            if chkTemp is 0:
                rushDomain.setHeuristic(next_state,rushDomain.h(next_state))
                # next_state[2]=rushDomain.h(next_state) #+ rushDomain.stateDepth(next_state)
                # printState(next_state)
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
        # rushDomain.printState(minstate)
        # print("h of minstate="+str(minstate[2]))
