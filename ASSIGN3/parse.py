import sys
import pdb
from bayes_networks import *
from variableElimination import *

def readFile(filename):
    try:
        f = open(filename)
        #input =  f.readlines()
        input = [line.strip() for line in open(filename)] #get all lines from file
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print("Unexpected error.")
        return -1
    finally:
        f.close()
    return input

def parseBN(input):

    listOfVars=dict()
    line=0

    while(line != len(input)):

        # parse variable
        if len(input[line]) > 0 and input[line][0] != '#' and 'VAR' in input[line]:
            var = bayesVar()

            varline = line+1

            while(input[varline] != ''):

                if 'name' in input[varline]:
                    var.setName(input[line+1].split(" ")[1])

                elif 'alias' in input[varline]:
                    var.setAlias(input[varline].split(" ")[1])

                elif 'parents' in input[varline]:
                    parents = input[varline].split(" ")
                    parents.pop(0)
                    var.setParents(parents)

                elif 'values' in input[varline]:
                    values = input[varline].split(" ")
                    values.pop(0)
                    var.setValues(values)

                varline += 1

            # add node to bayes network with both name and alias as keys
            listOfVars[var.name] = var
            if var.alias is not False:
                listOfVars[var.alias] = var

        line += 1

    line = 0
    while(line != len(input)):
        # parse Conditional Probability Table (CPT)
        if len(input[line]) > 0 and input[line][0] != '#' and 'CPT' in input[line]:

            variable = input[line+1].split(" ")[1] # line after CPT names variable
            variable = listOfVars[variable]        # gets bayes node from list

            # connect node to parents
            #variable.connectToParents(listOfVars)


            # first value is from variable, the rest from parents
            numberOfValues = 1 + variable.getNumParents()

            # CPT is represented as a dictionary
            # the key is a tuple with a value combination
            # the key's value is the probability
            cpt=dict()

            # the table is in one line
            if 'table' in input[line+2] and len('table') < len(input[line+2]):
                table = input[line+2].split(" ")
                table.pop(0)    # remove 'table' sting

                while(len(table) != 0):
                    values=list()
                    # get combination of values
                    for it in range(0,numberOfValues):
                        values.append(table.pop(0))
                    # tuple from value combination as key, probability as dictionary value
                    cpt[tuple(values)] = float(table.pop(0))

            elif 'table' in input[line+2] and len('table') == len(input[line+2]):

                cptLine = line + 3 # line iterator
                while(input[cptLine] != ''):
                    values=list()
                    table = input[cptLine].split(" ")

                    for it in range(0,numberOfValues):
                        values.append(table.pop(0))

                    cpt[tuple(values)] = float(table.pop(0))
                    cptLine += 1

            variable.setCPT(cpt)
        line += 1

    return listOfVars



if len(sys.argv) == 2:
    filename=str(sys.argv[1])
    verbose = False
elif len(sys.argv) == 3:
    filename=str(sys.argv[1])
    if sys.argv[2] == '-v':
        verbose = True
else:
    print("Correct usage:")
    print("-v for verbose mode")
    print("python program.py <filename> <-v>")
    sys.exit(1)

stuff=readFile("test.bn")
if stuff != -1:

    # for f in stuff:
    #     print f


    bayesNetwork = parseBN(stuff)

    connectedNodes=list()
    for f in bayesNetwork.values():
        if f not in connectedNodes:
            f.connectToParents(bayesNetwork)
            connectedNodes.append(f)

    # for f in bayesNetwork.values():
    #     f.Print()

    undirectedNetwork = dict()



    for node in bayesNetwork.values():
        if node not in undirectedNetwork.values():
            undirectedNetwork[node.name]=bayesUnVar(node)

    # build undirected graph
    for node in undirectedNetwork.values():
       # print '--------------------'
       # print node.ref.name
        node.connectUndirected(bayesNetwork,undirectedNetwork)
        # print 'undirected'
        # for un in node.Child + node.Parent + node.Neighbors:
        #     print un.ref.name


    #
    # calculate heuristic for variable elimination for every variable
    #
    varOrder = dict()
    for un in undirectedNetwork.values():
        varOrder[un.ref.name]=len(un.Child + un.Parent + un.Neighbors)


    # for key,value in varOrder.iteritems():
    #     print undirectedNetwork[key].ref.name, value

    # for key,value in bayesNetwork.iteritems():
    #     print '---------------------------'
    #     if len(key) > 1:
    #         value.Print()

    evidence = dict()
    query = list()
    # evidence['JohnCalls']='t'
    # evidence['MaryCalls']='t'
    #evidence['E']='t'

    # query = ['Burglary']
    while(True):
        while(True):
            queryInput = raw_input('Enter a query variable: ')
            if queryInput not in bayesNetwork.keys():
                print 'Variable does not exist in network.'
            else:
                query.append(queryInput)
                break

        while(True):
            evidenceVar = raw_input('Enter an evidence variable: ')
            if evidenceVar not in bayesNetwork.keys():
                print('Variable does not exist in network.')
                continue

            print 'Possible values for', evidenceVar, 'are', bayesNetwork[evidenceVar].values

            evidenceValue = raw_input('Enter the value for that variable: ')
            if evidenceValue not in bayesNetwork[evidenceVar].values:
                print('That value is not valid.')
                continue

            evidence[evidenceVar]=evidenceValue

            finished = raw_input('Finished query? (press enter to insert more evidence / write anything to execute)')
            if finished:
                break
            else:
                continue

        for i,var in enumerate(query):
            query[i]=bayesNetwork[var].name
            if bayesNetwork[var].name in varOrder.keys():
                del varOrder[bayesNetwork[var].name]

        for var in evidence.keys():
            if bayesNetwork[var].name in varOrder.keys():
                del varOrder[bayesNetwork[var].name]

        print 'query:',query
        print 'evidence', evidence.keys()
        print 'varOrder',varOrder.keys()
        varElim(bayesNetwork,query,evidence,varOrder,verbose)
