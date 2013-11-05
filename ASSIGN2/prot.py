def loadProblem(filename):
    input = [line.strip() for line in open(filename)] #get all lines from file
    input = [line for line in input if line] #delete blank lines
#    input = map(list,input) #seperate characters in string
    
    clauses = list()
    symbols = list()
    
    for l in input:
        # ignore comments
        if l[0] == 'c':
            continue
        # store information about the CNF problem
        elif l[0] == 'p':
            format = l[1]
            numberSymbols = int(l[2])
            numberClauses = int(l[3])
        # store clauses
        else:
            clauses.append(l)

    # store each symbol
    for x in range(1,numberSymbols+1):
        symbols.append(str(x))

    print(symbols)
    print(clauses)

loadProblem("cnf.txt")
