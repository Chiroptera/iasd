def varElim(Graph,query,evidence,varOrder):
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

    factors = dict()
    factorList = list()
    tempAdded = list()
    for node in Graph.values():
        if node not in tempAdded:
            tempAdded.append(node)
            tempFactor = node.getFactor()
            factorList.append(tempFactor)

            for var in tempFactor.vars:
                if var not in factors.keys():
                    factors[var]=list()
                factors[var].append(tempFactor)



    # for key,value in Graph.iteritems():
    #     if len(key) > 1:
    #         print '---------------------------'
    #         value.Print()
    #         factors.append(value)


    for f in factorList:
        f.Print()

    resultFactor=factorList[-1].pointwiseMul(factorList[-2])
    resultFactor.Print()
    a=resultFactor.sumOut('Alarm')
    a.Print()

    print '*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n*\n'

    # Now it's VE
    for var in varOrder:
        factorsList = eliminate(factorList,var)


    print 'its done'
    for f in factorList:
        f.Print()

def eliminate(Z,var):
    IN = list()
    OUT = list()

    for f in Z:
        if var in f.vars:
            IN.append(f)
        else:
            OUT.append(f)

    print '\n\n\n---------------------------------'
    print 'eliminating variable ', var
    print 'IN list is '
    for f in IN:
        f.Print()

    print 'OUT list is '
    for f in OUT:
        f.Print()


    resultingFactor = IN.pop()
    if len(IN) != 0:
        for f in IN:
            resultingFactor = resultingFactor.pointwiseMul(f)
            print 'pointwise\n'
            resultingFactor.Print()

    resultingFactor = resultingFactor.sumOut(var)

    print '\nafter sum out \n'
    resultingFactor.Print()



    return OUT.append(resultingFactor)
