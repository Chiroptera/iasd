from random import randint

class proposition:
    def __init__(self, numSymbols,numClauses,clauses):
        self.numSymbols = numSymbols
        self.numClauses = numClauses
        self.clauses = clauses

        # create dictionary and fill it with each symbol
        self.symbols=dict()
        for sym in range(1,numSymbols+1):
            self.symbols[sym] = []
    

    #################   FUNCTION   #############################
    # Name: setRandomSymbolTrueness
    # Input: self
    # Output: None
    # Description: assign random values (True of False) to
    #              every symbol
    #              
    #              
    ############################################################
    def setRandomSymbolTrueness(self):
        # for every symbol generate a random 1 or 0
        # if it's 1, add symbol to true list and its negation to false list
        # it it's 0, add symbol to false list and its negation to true list
        for sym in self.symbols:
            if randint(0,1) == 1:
                self.setSymbolValue(sym,True)
            else:
                self.setSymbolValue(sym,False)

    #################   FUNCTION   #############################
    # Name: 
    # Input: 
    # Output: 
    # Description: 
    #              
    #              
    #              
    ############################################################
    def setSymbolValue(self,symbol,value):
        self.symbols[symbol]=value

    #################   FUNCTION   #############################
    # Name: 
    # Input: 
    # Output: 
    # Description: 
    #              
    #              
    #              
    ############################################################

    def symbolValue(self,sym):
        return self.symbols[sym]

    def getSymbolValue(self,sym):
        value = self.symbols[abs(sym)]
        if sym < 0:
            return value
        else:
            return not value

    def isClauseTrue(self,clause):
        for sym in clause:
            if self.getSymbolValue(sym) is True:
                return True
        return False

    def isSatisfied(self):
        for clause in self.clauses:
            if self.isClauseTrue(clause) is False:
                return False
        return True

    def evalClauses(self):
        count = 0
        for clause in self.clauses:
            if self.isClauseTrue(clause) is True:
                count = count +1
        return count

    

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


    problem = proposition(numberSymbols,numberClauses,clauses)
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
        sentence.setRandomSymbolTrueness()

        for j in range(0,max_climbs):
            if sentence.isSatisfied() is True:
                return sentence
            
            # 1st element is the symbol, 2nd is the value
            bestSuccessor=[0,0]

            for sym in sentence.symbols.keys():
                sentence.setSymbolValue(sym,not sentence.symbolValue(sym)) # switch symbol value
                if sentence.evalClauses() > bestSuccessor[1]:
                    bestSuccessor = [sym,sentence.evalClauses()]
                sentence.setSymbolValue(sym,not sentence.symbolValue(sym)) # return original symbol value
            
            sentence.setSymbolValue(bestSuccessor[0],not sentence.symbolValue(bestSuccessor[0]))
    return False
            



prop=loadProblem("cnf.txt")
print(prop.symbols)
print(prop.clauses)

prop.setRandomSymbolTrueness()


a=GSAT(prop,1,1)
if a is False:
    print False
else:
    print True
    print a.symbols
