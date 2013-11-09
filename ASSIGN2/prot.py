from random import randint
from random import choice
from random import random

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
        for sym in self.symbols:
            self.setSymbolValue(sym,choice([True,False]))

    #################   FUNCTION   #############################
    # Name:
    # Input:
    # Output:
    # Description:
    #
    #
    #
    ############################################################

    def getSymbolValue(self,sym):
        value = self.symbols[abs(sym)]
        if sym > 0:
            return value
        else:
            return not value

    def switchSymbolValue(self,sym):
        self.symbols[abs(sym)] = not self.symbols[abs(sym)]

    def getSymbols(self):
        return self.symbols.keys()

    def getRandomFalseClause(self):
        falseClauses=list()

        # determine and store false clauses
        for clause in self.clauses:
            if not self.isClauseTrue():
                falseClauses.append(clause)

        # return random clause from false clause list
        return choise(falseClauses)

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

def saveProblem(filename,sentence):
    pass
# output file of CNF type should have .cnf extension
# format:
# c -comments
# s type solution variables clauses
# type is "max" for an input of cnf
# solution is 1 for satisfiable, 0 for not, -1 for no conclusion
#
# line t is optional
# t type solution variables clauses cpusecs measure1 ...
# type, solution, variables and clauses is the same as before
# cpusecs is the run time which can be in floating point notation
# measure 1 is mandatory even if it does nor represent anything -> 0


def WalkSAT(sentence,p,max_flips):
    # construct random model for sentence
    sentence.setRandomSymbolTrueness()

    for i in range(0,max_flips):
        # if sentence is satisfied, return sentence
        if sentence.isSatisfied(): return sentence

        # choose random false clause
        clause = sentence.getRandomFalseClause()

        # with probability p flip random symbol
        if random() < p:
            # flip random symbol in selected clause
            sentence.switch(choice(clause))
        else:
            # flip symbol in clause that maximizes true clauses
            bestSuccessor=[0,0]
            for sym in clause:
                # flip symbol
                sentence.switchSymbol(sym)

                # check model evaluation
                if sentence.evalClauses() > bestSuccessor[1]:
                    bestSuccessor=[sym,sentence.evalClauses()]

                # revert symbol's value to original
                sentence.switchSymbol(sym)

            # flip one of the symbols that yielded the best evaluation
            sentence.switchSymbol(bestSuccessor[0])

    return False

def GSAT(sentence,max_restarts,max_climbs):

    for i in range(0,max_restarts):
        # construct random model for sentence
        sentence.setRandomSymbolTrueness()

        for j in range(0,max_climbs):
            # if sentence is satisfied, return sentence
            if sentence.isSatisfied() is True:
                return sentence

            # 1st element is the symbol, 2nd is the value
            bestSuccessor=[0,0]

            for sym in sentence.getSymbols():
                # switch symbol value
                sentence.switchSymbolValue(sym)
                # checks if switching this symbol's value has better evaluation
                if sentence.evalClauses() > bestSuccessor[1]:
                    bestSuccessor = [sym,sentence.evalClauses()]
                # reverts symbol's value back to original
                sentence.switchSymbolValue(sym)

            # switch value for the symbol that yielded best evaluation
            sentence.switchSymbolValue(bestSuccessor[0])
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

b = WalkSAT(prop,0.6,10)
if b is False:
    print False
else:
    print True
    print b.symbols
