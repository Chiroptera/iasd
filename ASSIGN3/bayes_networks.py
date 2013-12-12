import pdb

class factor:
    def __init__(self,vars,CPT):
        self.vars = vars
        self.CPT = CPT

    def pointwiseMul(self,other):

        # get common variables
        commonVars = list(set(self.vars) & set(other.vars))
        if len(commonVars) == 0:
            print 'No common variables.'
            return

        finalVarsList = list(tuple(self.vars) + tuple([v for v in other.vars if v not in commonVars]))

        # outCPT[combLeft + ([v for i,v in enumerate(combRight) if i not in rightPos ]] = probLeft * progRight

        if len(self.CPT) > len(other.CPT):
            lenBiggestCPT = len(self.CPT)
            orderedFactor = [self,other]
        else:
            lenBiggestCPT = len(other.CPT)
            orderedFactor = [other,self]

        varsPos = dict()
        rightPos = list()       # list with the positions of all the common variables in the other's CPT
        for var in commonVars:
            varsPos[var]=(self.vars.index(var),other.vars.index(var)) # get position of variable in self and other variable list

            rightPos.append(other.vars.index(var))


        # to compute the new CPT we iterate over the entire CPT of the other factor for each combination of the self factor
        # if the values of the common variables match, than we multiply the its probabilities

        outCPT = dict()
        left = 0
        right = 1

        for combLeft,probLeft in self.CPT.iteritems():

            for combRight,probRight in other.CPT.iteritems():

                # check if common variables have the same value
                sameValue = True
                for var in commonVars:

                    # print 'varsPos[var] = ', varsPos[var]
                    # print 'varsPos[var][left] = ',varsPos[var][left]

                    if combLeft[varsPos[var][left]] != combRight[varsPos[var][right]]: # if one of the variables has different value we can stop
                        sameValue = False
                        break

                # next iteration of right table if common variables' values don't match
                if sameValue == False:
                    continue

                # from combRight remove the common variable assignment
                outCPT[combLeft + tuple([v for i,v in enumerate(combRight) if i not in rightPos ])] = probLeft * probRight

        return factor(finalVarsList,outCPT)

    def sumOut(self,var):
        varPos = self.vars.index(var)
        finalVarsList=[v for v in self.vars if v != var] # list with all the variables except the one to sum out

        print 'sum out\n\n'
        print finalVarsList
        outCPT = dict()

        for comb,prob in self.CPT.iteritems():
            newComb = tuple([v for i,v in enumerate(comb) if i != varPos])
            if newComb not in outCPT.keys():
                outCPT[newComb] = prob
            else:
                outCPT[newComb] += prob

        return factor(finalVarsList,outCPT)


    def Print(self):
        print 'Variables: '
        for var in self.vars:
            print '\t',var

        print 'CPT'
        for key,value in self.CPT.iteritems():
            print '\t', key,value


class bayesVar:

    def __init__(self):
        self.name = False
        self.alias = False
        self.parentsNames = []
        self.values = False
        self.undirected = list()
        self.childs = list()
        self.parents = list()
        self.CPT = 0

    def setName(self,name):
        self.name = name

    def setAlias(self,alias):
        self.alias = alias

    def setParents(self,parents):
        self.parentsNames=list(parents)

    def setValues(self,values):
        self.values = list(values)

    def setCPT(self,CPT):
        self.CPT = CPT

    def getFactor(self):
        allvars=list(self.parentsNames)
        allvars.insert(0,self.name)
        return factor(allvars,dict(self.CPT))

    def Print(self):
        print 'Name: ',self.name
        if self.alias: print 'Alias: ', self.alias
        if self.parentsNames != []:
            print 'Parents: ', self.parentsNames
        print 'Values: ', self.values
        print 'CPT'
        for key,value in self.CPT.iteritems():
            print '\t', key,value
        print 'Childs:'
        for c in self.childs:
            print '\t', c.name

    def connectToParents(self,setOfNodes):
        if self.parentsNames != []: # if there are parents
            for index,parent in enumerate(self.parentsNames):
                self.parents.append(setOfNodes[parent]) #put parent in this node's parents list
                setOfNodes[parent].childs.append(self) # put current node in parent's child list

                if parent == setOfNodes[parent].alias:
                    self.parentsNames[index] = setOfNodes[parent].name


    def getNumParents(self):
        return len(self.parentsNames)


# bayes undirected variable
class bayesUnVar:
    def __init__(self,realnode):
        self.ref = realnode
        self.Child = list()
        self.Parent = list()
        self.Neighbors = list()

    def connectUndirected(self,graph,unGraph):
        for c in self.ref.childs:
            self.Child.append(unGraph[c.name])

        for (i,p) in enumerate(self.ref.parents):
            self.Parent.append(unGraph[p.name])

            for parent in self.ref.parents[:i] + self.ref.parents[(i+1):]:
                unGraph[p.name].Neighbors.append(unGraph[parent.name])

        #l_without_num = l[:k] + l[(k + 1):] list with every element except the Kth

    def removeNode(self,unGraph):
        for neighbor in self.Neighbors:
            neighbor.Neighbors.remove(self) # remove itself from neighbors

            for parent in self.Parent:
                parent.Child.remove(self) # remove itself from parents

                for child in self.Child:
                    child.Parent.remove(self) # remove itself from childs
                    child.Parent.append(parent) # link childs to parents
                    parent.Child.append(child)  # link parents to childog
