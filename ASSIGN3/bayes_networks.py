class bayesVar:

    def __init__(self,name):
        self.name = False
        self.alias = False
        self.parents = []
        self.values = False

    def setAlias(self,alias):
        self.alias = alias

    def setParents(self,parents):
        self.parents=list(parents)

    def setValues(self,values):
        self.values = list(values)

    def setCPT(self,CPT):
        self.CPT = CPT

    def Print(self):
        for f in [self.name,self.alias,self.parents,self.values]:
            if f is not False and f is not []:
                print f


class CPT:
    pass

class network:
    pass
