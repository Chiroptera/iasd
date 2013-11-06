from random import randint

class proposition:
    def __init__(self, numSymbols,numClauses,symbols,clauses):
        self.numSymbols = numSymbols
        self.numClauses = numClauses
        self.symbols = symbols
        self.clauses = clauses

    def setSymbolTrueness(self):
        # create lists to store which symbols are true or false
        self.symTrue = list()
        self.symFalse = list()

        # for every symbol generate a random 1 or 0
        # if it's 1, add symbol to true list and its negation to false list
        # it it's 0, add symbol to false list and its negation to true list
        for sym in self.symbols:
            if randint(0,1) == 1:
                self.symTrue.append(sym)
                self.symFalse.append(-sym)
            else:
                self.symFalse.append(sym)
                self.symTrue.append(-sym)

    def isSymbolTrue(self,sym):
        if sym not in self.symbols:
            raise NameError("Symbol doesn't exist.")
        if sym in self.symTrue:
            return True

    def isClauseTrue(self,clause):
        for sym in clause:
            if sym in self.symTrue:
                return True
        return False

def loadProblem(filename):
    input = [line.strip() for line in open(filename)] #get all lines from file
    input = [line for line in input if line] #delete blank lines
    #input = map(list,input) #seperate characters in string


    clauses = list()
    symbols = list()

    print input

    for l in input:
        # ignore comments
        if l[0] == 'c':
            continue
        # store information about the CNF problem
        elif l[0] == 'p':
            l=l.split(" ")
            print l
            format = l[1]
            numberSymbols = int(l[2])
            numberClauses = int(l[3])
        # store clauses
        else:
            l=l.split(" ")
            del l[-1]
            for i in range(0,len(l)):
                l[i]=int(l[i])
            clauses.append(l)

    # store each symbol
    for x in range(1,numberSymbols+1):
        symbols.append(x)

    problem = proposition(numberSymbols,numberClauses,symbols,clauses)
    return problem


# function GSAT(sentence, max-restarts, max-climbs) returns a truth assign-
# ment or failure
# for i <- 1 to max-restarts do
# A <- A randomly generated truth assignment
# for j <- 1 to max-climbs do
# if A satisfies sentence then return A
# A <- a random choice of one of the best successors of A
# end
# end
# return failure


def GSAT(sentence,max_restarts,max_climbs):

    for i in range(0,max_restarts):
        sentence.setSymbolTrueness()

        for j in range(0,max_climbs):
            pass



prop=loadProblem("cnf.txt")
print(prop.symbols)
print(prop.clauses)

prop.setSymbolTrueness()
print(prop.symTrue)
print(prop.symFalse)
prop.isSymbolTrue(7)
