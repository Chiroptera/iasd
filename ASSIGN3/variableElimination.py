def varElim(Graph,query,evidence,varOrder,verbose=False):
    # Graph is a dictionary with alias and names for keys; bayes nodes for values
    # Query is the name of a variable
    # Evidence is a dictionary with variable names for keys; assignment for values
    # unGraph is a dictionary with names for keys; undirected bayes nodes for values


    #
    # simplifying the CPTs with the evidence
    #
    for key,value in evidence.iteritems():
        # remove probabilities of non-evidence from evidence nodes
        for line in Graph[key].CPT.keys():
            if line[0] != value:
                del Graph[key].CPT[line]

        # remove probabilities of non-evidence from evidence's child nodes
        for child in Graph[key].childs:

            # try to get a position in which the evidence values appear
            try:
                pos = child.parentsNames.index(Graph[key].name)
            except:
                pos = child.parentsNames.index(Graph[key].alias)

            # remove the probabilities
            for line in child.CPT.keys():
                if line[pos+1] != value:
                    del child.CPT[line]


    #
    # filling the factor list
    #

    factorList = list()
    tempAdded = list()
    for node in Graph.values():
        if node not in tempAdded:
            tempAdded.append(node)
            tempFactor = node.getFactor()
            factorList.append(tempFactor)


    # Now it's VE
    if verbose:
        print '\n-----------------------------------------------------------'
        print 'Starting Variable Elimination procedure...'
    for var in varOrder:
        factorList = eliminate(factorList,var,verbose)

    if verbose:
        print 'Computing pointwise multiplication between resulting factors...'

    resultFactor = factorList.pop()

    for f in factorList:
        if verbose:
            print '\n\nMultiplication between factors'
            resultFactor.Print()
            print '\nand\n'
            f.Print()

        resultFactor = resultFactor.pointwiseMul(f)

        if verbose:
            print 'The result was:'
            resultFactor.Print()


    normalizeK = sum(resultFactor.CPT.values())
    for comb,prob in resultFactor.CPT.iteritems():
        resultFactor.CPT[comb]=prob / normalizeK

    if verbose:
        print '\n\nNormalizing...'
        print 'Normalizing constant is', normalizeK
        print 'Factor normalized is:'
        resultFactor.Print()

    resultFactor.printProb(query[0])

def eliminate(Z,var,verbose):
    IN = list()
    OUT = list()

    for f in Z:
        if var in f.vars:
            IN.append(f)
        else:
            OUT.append(f)

    if verbose:
        print '\n\n\n--------------------'
        print '\t********************************************'
        print '\t*       ELIMINATE VARIABLE                 *'
        print '\t*\t\t',var
        print '\t*                                          *'
        print '\t********************************************'
        print 'Factors involved are'
        for f in IN:
            f.Print()
        print '\n---------------------'

    resultingFactor = IN.pop()
    if len(IN) != 0:
        for f in IN:

            if verbose:
                print 'Doing pointwise multuplication between factors '
                resultingFactor.Print()
                print '\nand\n'
                f.Print()

            resultingFactor = resultingFactor.pointwiseMul(f)

            if verbose:
                print 'The result was:'
                resultingFactor.Print()

    if verbose:
        print 'Doing sum-out...'

    resultingFactor = resultingFactor.sumOut(var)

    if verbose:
        print 'The result was:'
        resultingFactor.Print()


    OUT.append(resultingFactor)

    if verbose:
        print '\n\nThe returning list of factor is:'
        for f in OUT:
            f.Print()

    return OUT
