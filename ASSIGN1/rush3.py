import rushDomain

def generalSearch(problem):

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
        #printState(current_state[-1])
        current_actions=rushDomain.actions(current_state) # determine actions available fo current state

#        print("Possible actions for this state="+str(current_actions))
#        raw_input("continue")

        for x in current_actions: #for each action
            next_state=rushDomain.results(current_state,x) # determine its result

            if rushDomain.goaltest(next_state) is True: # if result is goal
                paths.append(rushDomain.buildPath(next_state)) # calculate path to result and add it to paths
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
                if rushDomain.cmpStates(next_state,exp):
                    #printState(exp[-1])
                    #print next_state
                    #printState(next_state[-1])
                    #raw_input("continue...")
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
