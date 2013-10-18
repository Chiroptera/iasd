import sys
import rush3
import time

if len(sys.argv) == 2:
    cmdargs=str(sys.argv)
else:
   sys.exit("Correct usage: python program.py filename")

# parse name of file of problem
filename_read=str(sys.argv[1])

print("Loading problem from file",filename_read)
problem=rush3.loadProblem(filename_read)


print("Solving problem from file",filename_read)
start=time.time() # store start time for runtime computation
solution=rush3.generalSearch(problem[0],problem[-1]) # problem[0]=problem
                                                     # problem[1]=problemSize 
# compute search runtime
runtime=time.time()-start

print("Problem from file "+filename_read+" solved in "+str(runtime)+" s")

# create name for solution file
filename_write=filename_read+".sol"

try:
    # This will create a new file or **overwrite an existing file**.
    f = open(filename_write, "w")
    try:
        #f.write("Runtime: "+str(runtime)+"s"+"\n")
        #f.write("Solutions found: "+str(len(solution))+"\n")
        for num,sol in enumerate(solution):
            #f.write("----- Num"+str(num)+" -----"+"\n")

            #f.write("Pathcost: "+str(len(sol))+"\n")
            f.write(str(len(sol))+"\n")
            #f.write("Path:")
            for move in sol:
                f.write(move[0]+move[1]+str(move[2])+"\n")
    #    f.writelines(lines) # Write a sequence of strings to a file
    finally:
        f.close()
        print("Solution of problem from file "+filename_read+" stored in file "+filename_write)
except IOError:
    print("There was a error writing to file.")
