import sys
from bayes_networks import *


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
            variable.connectToParents(listOfVars)

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
            print variable.CPT
        line += 1

    return listOfVars


if len(sys.argv) == 2:
    filename=str(sys.argv[1])
else:
    print("Correct usage:")
    print("python program.py filename")
    sys.exit(1)

stuff=readFile("test.bn")
if stuff != -1:

    for f in stuff:
        print f

    bayesNetwork = parseBN(stuff)

    for (key,value) in bayesNetwork.iteritems():
        print '---------------------------'
        value.Print()
