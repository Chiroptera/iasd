class bayesVar:

    def __init__(self):
        self.name = False
        self.alias = False
        self.parentsNames = []
        self.values = False

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
            print key,value

    def connectToParents(self,setOfNodes):
        if self.parentsNames != []:
            self.parents=list()
            for parent in self.parentsNames:
                self.parents.append(setOfNodes[parent])

    def getNumParents(self):
        return len(self.parentsNames)
