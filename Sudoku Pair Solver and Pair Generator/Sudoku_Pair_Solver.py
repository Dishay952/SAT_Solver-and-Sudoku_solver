from pysat.solvers import Glucose3
import numpy as np
import csv
solver=Glucose3()

k=int(input("Enter the size of the sudoku subgrid:"))
filename=input("Enter the filename of the CSV file containing the unsolved sudoku pair, make sure it is in the same directory as this file:")


with open(filename,'r',encoding='utf-8-sig') as f:
    sudokuraw=np.genfromtxt(f,delimiter=',')

sudoku=np.empty((2,k*k,k*k))
sudoku[0]=sudokuraw[0:k*k][:]
sudoku[1]=sudokuraw[k*k:][:]

#Adds all the initial numbers to the solver
for x in range(2):
    for i in range(k*k):
        for j in range(k*k):
            for y in range(1,k*k+1):
                if(sudoku[x][i][j]==y):
                    solver.add_clause([y+k*k*j+(k**4)*i+(k**6)*x])

#CONSTRAINTS
#1) There is atleast 1 number in each entry
#2) Each number appears exactly once in each row
#3) Each number appears exactly once in each column
#4) Each number appears exactly once in each kxk sub-grid

for x in range(2):
    for i in range(k*k):
        for j in range(k*k):
            propositions=[]
            for y in range(1,k*k+1):
                propositions.append(y+k*k*j+((k*k)**2)*i+((k*k)**3)*x)
                for z in range(y+1,k*k+1):
                    solver.add_clause([-1*(y+k*k*j+((k*k)**2)*i+((k*k)**3)*x),-1*(z+k*k*j+((k*k)**2)*i+((k*k)**3)*x)])
            solver.add_clause(propositions)

for x in range(2):
    for j in range(k*k):
        for y in range(1,k*k+1):
            propositions=[]
            for i in range(k*k):
                propositions.append(y+k*k*j+((k*k)**2)*i+((k*k)**3)*x)
                for z in range(i+1,k*k):
                    solver.add_clause([-1*(y+k*k*j+((k*k)**2)*i+((k*k)**3)*x),-1*(y+k*k*j+((k*k)**2)*z+((k*k)**3)*x)])
            solver.add_clause(propositions)

for x in range(2):
    for i in range(k*k):
        for y in range(1,k*k+1):
            propositions=[]
            for j in range(k*k):
                propositions.append(y+k*k*j+((k*k)**2)*i+((k*k)**3)*x)
                for z in range(j+1,k*k):
                    solver.add_clause([-1*(y+k*k*j+((k*k)**2)*i+((k*k)**3)*x),-1*(y+k*k*z+((k*k)**2)*i+((k*k)**3)*x)])
            solver.add_clause(propositions)

for x in range(2):
    for y in range(1,k*k+1):
        for gridi in range(k):
            for gridj in range(k):
                propositions=[]
                for celli in range(k):
                    for cellj in range(k):
                        propositions.append(y+(k**2)*(k*gridj+cellj)+(k**4)*(k*gridi+celli)+(k**6)*x)
                        for m in range(celli+1,k):
                            for n in range(cellj+1,k):
                                solver.add_clause([-1*(y+(k**2)*(k*gridj+cellj)+(k**4)*(k*gridi+celli)+(k**6)*x),-1*(y+(k**2)*(k*gridj+n)+(k**4)*(k*gridi+m)+(k**6)*x)])
                solver.add_clause(propositions)

for y in range(1,k*k+1):
    for i in range(k*k):
        for j in range(k*k):
            solver.add_clause([-1*(y+k*k*j+((k*k)**2)*i),-1*(y+k*k*j+((k*k)**2)*i+(k*k)**3)])

if(solver.solve()):
    ans=solver.get_model()

    pos=[]
    for x in ans:
        if(x>0):
            y=x%(k*k)
            if(y==0):
                y=k*k
            pos.append(y)

    pos=np.array(pos)

    solved=pos.reshape(2*k*k,k*k)
    with open('solved.csv','w',newline='') as file :
        mywriter=csv.writer(file,delimiter=',')
        mywriter.writerows(solved)
    print("Check solved.csv file")
    solved=pos.reshape(2,k*k,k*k)
    print("The first solved Sudoku is:")
    for row in solved[0]:
        print(row)
    print("The second solved Sudoku is:")
    for row in solved[1]:
        print(row)
else:
    print("None")
