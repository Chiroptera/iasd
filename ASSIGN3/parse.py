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

        if len(input[line]) > 0 and input[line][0] != '#' and 'VAR' in input[line]:
            var = bayesVar(input[line+1].split(" ")[1])
            varline = line+2

            while(input[varline] != ''):

                if 'alias' in input[varline]:
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

            print var.Print()

            listOfVars[var.name] = var
            if var.alias is not False:
                listOfVars[var.alias] = var

        if len(input[line]) > 0 and input[line][0] != '#' and 'CPT' in input[line]:
            print input[line+1]
            variable = input[line+1].split(" ")[1]
            variable = listOfVars[variable]

            # the table is in one line
            if 'table' in input[line+2] and len('table') < len(input[line+2]):
                table = input[line+2].split(" ")
                table.pop(0)

                # first value is from variable, the rest from parents
                numberOfValues = 1 + len(variable.parents)

                cpt=dict()

                while(len(table) != 0):
                    values=list()
                    for it in range(0,numberOfValues):
                        values.append(table.pop(0))
                    cpt[tuple(values)] = float(table.pop(0))
                    print cpt

        line += 1


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

    parseBN(stuff)
