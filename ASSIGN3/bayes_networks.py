class bayesVar:

    def __init__(self):
        self.name = False
        self.alias = False
        self.parentsNames = []
        self.values = False
        self.undirected = list()
        self.childs = list()
        self.parents = list()

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
        if self.parentsNames != []:
            for parent in self.parentsNames:
                self.parents.append(setOfNodes[parent]) #put parent in this node's parents list
                setOfNodes[parent].childs.append(self) # put current node in parent's child list


    def getNumParents(self):
        return len(self.parentsNames)






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
                    parent.Child.append(child)  # link parents to childsg

class factor:
    def __init__(self,vars,CPT):
        self.vars=vars
        self.CPT

    def pointwise_mul(self,other,)
