from random import choice

####################### Function ##################
#
# Name: DPLL
# Input: clauses, is a list
##	 model, is a dictionary
# Output: True or False + model
# Description:
#
#
#
#
###################################################


def DPLL(sentence):
        # DEBUG
        # print("Symbols:" + str(sentence.symbols))
        # print("clauses" + str(sentence.clauses))
        # raw_input("--------------------------START----------------------")
        # DEBUG

	# if sentence is satisfied, return true
        if sentence.isSatisfied():
                return sentence
        # if some clause false, return false
	if sentence.isUnsatisfied():
		return False

	# PURE SYMBOL?
        pureSymbol = pure(sentence)
        if pureSymbol is not False:

                # assign value to pure symbol
                sentence.setSymbolValue(pureSymbol,True)

                # remove irrelevant clauses
                for clause in sentence.clauses:
                        if pureSymbol in clause:
                                sentence.clauses.remove(clause)
                # call DPLL
                return DPLL(sentence.copy())

        # UNIT CLAUSE?
	unitSymbol = unit(sentence)
	if unitSymbol is not False: #if unit symbol

		# assign value to unit symbol
		sentence.setSymbolValue(unitSymbol,True)

		# remove irrelevant clauses
                for clause in sentence.clauses:
                        if unitSymbol in clause:
                                sentence.clauses.remove(clause)
                # call DPLL
                return DPLL(sentence.copy())

        # get unassign symbols and pick the first one
        for sym in sentence.getSymbols():
                if sentence.getSymbolValue(sym) == []:
 			otherSymbol = sym
			break
	return (DPLL(sentence.copy().setSymbolValue(otherSymbol,True)) or DPLL(sentence.copy().setSymbolValue(otherSymbol,False)))






####################### Function ##################
#
# Name: pure
# Input: sentence, which consists of:
#	 clauses, is a list
#	 model, is a dictionary
# Output: A pure symbol or False
# Description: evaluates pure symbols and returns
# the variable that is a pure symbol or False if
# there is no pure symbol
#
###################################################
def pure(sentence):
        unass = list()
        for symbol in sentence.getSymbols():
                if sentence.symbols[symbol] is []:
                        unass.append(symbol)

        for symbol in unass:
                positiveCount = 0 # counter for number of times symbol appears
                negativeCount = 0 # counter for number of times negation of symbol appears
                for clause in sentence.clauses():
                        if symbol in clause:
                                positiveCount = positiveCount + 1
                        if -symbol in clause:
                                negativeCount = negativeCount + 1
                        if positiveCount != 0 and negativeCount != 0:
                                break
                if positiveCount == 0:
                        return -symbol
                elif negativeCount == 0:
                        return symbol
        return False




####################### Function ##################
#
# Name: unit
# Input: sentence which consists of:
#	 clauses, a list
#	 model, a dictionary
# Output: A unit clause or False
# Description: evaluates unit clauses and returns
# the variable that is a unit clause or False if
# there are no unit clause
#
###################################################
def unit(sentence):
	for i in sentence.clauses:		#for every clause
		if len(i) is 1:	#only one literal
			#return value
			return i[0]

		#check if all literals except one is false in a clause
		c = 0
                unit2 = []
		for j in i:
                        j_val= sentence.getSymbolValue(j)
                        if j_val is False:
                                c = c + 1
                        elif j_val:
                                break
                        else:
                                unit2.append(j)

			# if j>0:	#if positive
			# 	if sentence.getSymbolValue(j) is False:
			# 		c = c+1
			# 	elif sentence.getSymbolValue(j) is True:
			# 		break
			# 	else:
			# 		unit2 = j	#which literal is not assigned false
			# else:
			# 	if sentence.getSymbolValue(j) is True:
			# 		c = c+1
			# 	elif sentence.getSymbolValue(j) is False:
			# 		break
			# 	else:
			# 		unit2 = j	#which literal is not assigned false
                #if len(unit2) == 1:
		if c is (len(i)-1) and len(unit2) == 1: #if all literals but one is false
                #if c == (len(i)-1):
			#return value
                        return unit2[0]
	#if no unit clause is found
	return False
