from random import randint
from random import choice
from random import random
import sys
from time import time
from DPLL import DPLL

    #################   FUNCTION   #############################
    # Name: absg
    # Input: value
    # Output: absolute of value
    # Description: simple function to compute the absolute of
    #              a value - reduces delays compared with
    #              builtin function
    #
    ############################################################

def absg(value):
    if value > 0:
        return value
    else:
        return -value

class proposition:
    def __init__(self, numSymbols,numClauses,clauses):
        self.numSymbols = numSymbols
        self.numClauses = numClauses
        self.clauses = clauses

        # create dictionary and fill it with each symbol
        self.symbols=dict()

    #################   CLASS METHOD   #########################
    # Name: fillSymbols
    # Input: self
    # Output: None
    # Description: from number of symbols fills symbol dictionary
    #
    ############################################################

    def fillSymbols(self):
        for sym in range(1,self.numSymbols+1):
            self.symbols[sym] = []

    #################   CLASS METHOD   #########################
    # Name: setRandomSymbolTrueness
    # Input: self
    # Output: None
    # Description: assign random values (True of False) to
    #              every symbol
    #
    ############################################################

    def setRandomSymbolTrueness(self):
        for sym in self.symbols:
            self.symbols[sym]=choice([True,False])

    #################   CLASS METHOD   #########################
    # Name: setSymbolValue
    # Input: self,symbol, value
    # Output: sentence
    # Description: receives a symbol or its negation and sets
    #              the symbol value to the designated value
    #
    ############################################################

    def setSymbolValue(self,sym,value):
        if sym > 0:
            self.symbols[sym] = value
        else:
            self.symbols[-sym] = not value
        return self

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def getSymbolValue(self,sym):
        value = self.symbols[absg(sym)]
        if value == []:
            return []
        if sym > 0:
            return value
        else:
            return not value

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def switchSymbolValue(self,sym):
        self.symbols[absg(sym)] = not self.symbols[absg(sym)]

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def getSymbols(self):
        return self.symbols.keys()

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def getRandomFalseClause(self):
        falseClauses=list()

        # determine and store false clauses
        for clause in self.clauses:
            if self.isClauseFalse(clause):
                falseClauses.append(clause)

        # return random clause from false clause list
        return choice(falseClauses)

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def isClauseTrue(self,clause):
        for sym in clause:
            if self.getSymbolValue(sym) is True:
                return True
        return False

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def isClauseFalse(self,clause):
        for sym in clause:
            if self.getSymbolValue(sym) is not False:
                return False
        return True

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def isSatisfied(self):
        for clause in self.clauses:
            if self.isClauseTrue(clause) is False:
                return False
        return True

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def isUnsatisfied(self):
        for clause in self.clauses:
            if self.isClauseFalse(clause):
                return True
        return False

    #################   CLASS METHOD   #########################
    # Name: getSymbolValue
    # Input: self,symbol
    # Output: symbol value
    # Description: receives a symbol or its negation and
    #              returns corresponding value
    #
    ############################################################

    def evalClauses(self):
        count = 0
        for clause in self.clauses:
            if self.isClauseTrue(clause) is True:
                count = count +1
        return count

    #################   CLASS METHOD   #########################
    # Name: copy
    # Input: self
    # Output: copy of self
    # Description: makes a copy of object
    #
    ############################################################

    def copy(self):
        newProp = proposition(self.numSymbols,self.numClauses,list(self.clauses))
        newProp.symbols = dict(self.symbols)
        return newProp


#################   FUNCTION   #############################
# Name: loadProblem
# Input: filename
# Output: sentence
# Description:
#
############################################################

def loadProblem(filename):
    input = [line.strip() for line in open(filename)] #get all lines from file
    input = [line for line in input if line] #delete blank lines
    #input = map(list,input) #seperate characters in string


    clauses = list()

    symbols = list()

    for l in input:
        # ignore comments
        if l[0] == 'c':
            continue
        # store information about the CNF problem
        elif l[0] == 'p':
            l=l.split(" ")
            while '' in l:      # remove null elements from list - important for correct parsing
                l.remove('')
            print(str(l))
            numberSymbols = int(l[2])
            numberClauses = int(l[3])
        elif l[0] == '%':
            break
        # store clauses
        else:
            l=l.split(" ")
            del l[-1]           # deletes clause terminating 0
            for i in range(0,len(l)):
                l[i]=int(l[i])
            clauses.append(l)


    problem = proposition(numberSymbols,numberClauses,clauses)
    problem.fillSymbols()
    return problem

def saveProblem(filename,sentence,runtime,algorithm):


        # create name for solution file
        filename_write = filename + "." + algorithm

        try:
            # This will create a new file or **overwrite an existing file**.
            fs = open(filename_write, "w")

            try:
                fs.write("c \n")
                fs.write("c ALGORITHM: " + algorithm + "\n")
                if sentence is False:
                    fs.write("c FAIL")
                fs.write("c \n")
                fs.write("p max " + str(sentence.numSymbols) + " " + str(sentence.numClauses) + "\n")
                fs.write("t max " + str(sentence.numSymbols) + " " + str(sentence.numClauses) + " " + str(runtime) + " " + str(float(sentence.numClauses)/sentence.numSymbols) + " " + "0\n")
            finally:
                fs.close()
                print("Solution saved in " + filename_write)
        except IOError:
            print("There was a error writing to file.")
            return -1


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
            sentence.switchSymbolValue(choice(clause))
        else:
            # flip symbol in clause that maximizes true clauses
            bestSuccessor=[0,0]
            for sym in clause:
                # flip symbol
                sentence.switchSymbolValue(sym)

                # check model evaluation
                if sentence.evalClauses() > bestSuccessor[1]:
                    bestSuccessor=[sym,sentence.evalClauses()]

                # revert symbol's value to original
                sentence.switchSymbolValue(sym)

            # flip one of the symbols that yielded the best evaluation
            sentence.switchSymbolValue(bestSuccessor[0])

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


if len(sys.argv) <= 3 and len(sys.argv) > 1:
    cmdargs=str(sys.argv)
else:
    print("Correct usage:")
    print("python program.py filename with default for heuristic search.")
    sys.exit(1)

filename = str(sys.argv[1])

problem=loadProblem(filename)
print("==========================================================")
print("====================== SAT SOLVER ========================")
print("==========================================================")
print(problem.symbols)
print(problem.clauses)

print("........:::::::: GSAT ::::::::........")
runtimeGSAT = time()
problemGSAT = GSAT(problem.copy(),2*problem.numSymbols,4*problem.numSymbols)
runtimeGSAT = time() -  runtimeGSAT
print("GnSAT runtime: " + str(runtimeGSAT) + "s")
if problemGSAT is False:
    print(str(False))
else:
    print(str(True))
    print(str(problemGSAT.symbols))

print("........:::::::: WalkSAT ::::::::........")
runtimeWSAT = time()
problemWSAT = WalkSAT(problem.copy(),0.6,5*problem.numSymbols)
runtimeWSAT = time() - runtimeWSAT
print("WalkSAT runtime: " + str(runtimeWSAT) + "s")
if problemWSAT is False:
    print False
else:
    print True
    print problemWSAT.symbols

print("........:::::::: DPLL ::::::::........")
runtimeDPLL = time()
print(str(problem.symbols))
problemDPLL = DPLL(problem.copy())
runtimeDPLL = time() - runtimeDPLL
print("DPLL runtime: " + str(runtimeDPLL) + "s")
if problemDPLL is False:
    print False
else:
    print True
    print problemDPLL.symbols

saveProblem(filename,problemGSAT,runtimeGSAT,"GSAT")
saveProblem(filename,problemWSAT,runtimeWSAT,"WSAT")
saveProblem(filename,problemDPLL,runtimeDPLL,"DPLL")
