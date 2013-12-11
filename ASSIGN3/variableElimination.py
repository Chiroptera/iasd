def varElim(Graph,query,evidence,unGraph):
    # Graph is a dictionary with alias and names for keys; bayes nodes for values
    # Query is the name of a variable
    # Evidence is a dictionary with variable names for keys; assignment for values
    # unGraph is a dictionary with names for keys; undirected bayes nodes for values

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

    factors = list()

    for key,value in Graph.iteritems():
        if len(key) > 1:
            print '---------------------------'
            value.Print()
            factors.append(value)

def eliminate(Z,factors):
    IN = list()
    OUT = list()

    IN.append(Z)
    for p in Z.parents:
        IN.append(p)
