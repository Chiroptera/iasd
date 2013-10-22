import sys
import rushDomain
import rush3
import rushA
import time

print("---------------- RUSH HOUR SOLVER ----------------")

if len(sys.argv) <= 3 and len(sys.argv) > 1:
    cmdargs=str(sys.argv)
else:
    print("Correct usage:")
    print("python program.py filename with default for heuristic search.")
    print("python proglram.py filename -h/-s for heuristic or simple search")
    sys.exit(1)


# parse name of file of problem
filename_read=str(sys.argv[1])

print("File: "+filename_read)
print("Loading problem from file.")
problem=rushDomain.loadProblem(filename_read)

start=time.time() # store start time for runtime computation

if len(sys.argv) == 3 and str(sys.argv[2]) == "-s":
    print("Solving problem using simple search.")
    solution=rush3.generalSearch(problem) # problem[0]=problem
                                          # problem[1]=problemSize
else:
    print("Solving problem using heuristic search.")
    solution=rushA.generalSearch(problem)


# compute search runtime
runtime=time.time()-start

if solution is not False:
    print("Problem solved in "+str(runtime)+" s")

    # create name for solution file
    filename_write=filename_read+".sol"
    file_stats=filename_read+".stats"

    try:
        # This will create a new file or **overwrite an existing file**.
        f = open(filename_write, "w")
        fs = open(file_stats,"w")
        try:
	    sol=solution[0]     # real solution is stored in first element of received list
            fs.write("Runtime: "+str(runtime)+"s"+"\n")
            fs.write("Path length: ")
            fs.write(str(len(sol))+"\n")
	    fs.write("Nodes generated: " + str(solution[1])+"\n")
	    fs.write("Average branching factor: " + str(solution[-1]))

            f.write(str(len(sol))+"\n")
            for move in sol:
                f.write(move[0]+move[1]+str(move[2])+"\n")

        finally:
            f.close()
            fs.close()
            print("Solution saved in "+filename_write)
            print("Statistics saved in "+file_stats)
    except IOError:
        print("There was a error writing to file.")
else:
    print("No solution found.")
