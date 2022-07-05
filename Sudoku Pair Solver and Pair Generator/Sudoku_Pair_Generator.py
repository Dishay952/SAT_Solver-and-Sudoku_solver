from pysat.solvers import Glucose3
import numpy as np
import random
import copy 
import csv
k=int(input("Enter the size of the sudoku subgrid:"))
sudoku=np.empty((2,k*k,k*k))

def sudoku_solve_first(sudokuraw,k):
    solver=Glucose3()
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
    
    ans=solver.solve()
    return solver.get_model()


def sudoku_solve(sudokuraw,k):
    solver=Glucose3()
    for x in range(2):
        for i in range(k*k):
            for j in range(k*k):
                for y in range(1,k*k+1):
                    if(sudokuraw[y-1+k*k*j+(k**4)*i+(k**6)*x]>0):
                        solver.add_clause([y+k*k*j+(k**4)*i+(k**6)*x])
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
    
    i=0
    for x in solver.enum_models():
        ans=np.array(x,dtype=float)
        i=i+1
    return (ans,i)


sudoku_init=np.empty(2*(k**6))
sudoku_init1=np.empty(2*(k**6))
sudoku_init2=np.empty(2*(k**6))
sudoku_init[:]=np.nan
sudoku_init=sudoku_solve_first(sudoku_init,k)


cell_list=list(range(0,2*(k**4)))
random.shuffle(cell_list)
while(bool(cell_list)):
    sudoku_init1=copy.deepcopy(sudoku_init)
    remove_index=cell_list[0]
    cell_list.remove(remove_index)
    for x in range(remove_index*(k**2),(remove_index+1)*(k**2)):
        sudoku_init1[x]=np.nan
    ans,count=sudoku_solve(sudoku_init1,k)
    if(count==1):
        sudoku_init=copy.deepcopy(sudoku_init1)    

final_ans=sudoku_init


number_list=list(range(1,k*k+1))
random.shuffle(number_list)

pos=[]
flag=0
for i in range(len(final_ans)):
    if(np.isnan(final_ans[i])):
        final_ans[i]=0
        flag=flag+1
        if(flag==1):
            pos.append(0)
        if(flag==k*k):
            flag=0
    else:
        x=int(final_ans[i])
        if(x>0):
            y=x%(k*k)
            if(y==0):
                y=k*k
            pos.append(number_list[y-1])


pos=np.array(pos)

solved=pos.reshape(2,k*k,k*k)

print("The first unsolved Sudoku is:")
for row in solved[0]:
    print(row)
print("The second unsolved Sudoku is:")
for row in solved[1]:
    print(row)

solved=solved.reshape(2*k*k,k*k)
with open('genSudoku.csv','w',newline='') as file :
    mywriter=csv.writer(file,delimiter=',')
    mywriter.writerows(solved)

