import numpy as np


# Open the file in read mode
with open('rich_mat.txt', 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

n_act = (0,0)

mat_dict = {}

for i in range(0,2):
    for j in range (0,9):
        mat_dict[(i,j)] = np.zeros(shape=(3,3))

for k in range(len(lines)):
    line = lines[k]

    for p in range(0,5):
        if (p == 1 or p == 3):
            continue
        for q in range (0,3):       
                n_act = (p,q) 

                s = line.split()
                
                if (len(s) == 2 and int(s[0]) == n_act[0] and int(s[1]) == n_act[1]):
                                        
                    for i in range(0,3):
                        for j in range (1,9):
                            
                            split = lines[k+i*8+j].split()
                            if (float(split[2]) < 1e-3):
                                continue
                            
                            if (p == 0):
                                mat_dict[(i,j-1)][n_act[0]][n_act[1]] =  float(split[2])
                                
                            if (p == 2):
                                mat_dict[(i,j-1)][1][n_act[1]] =  float(split[2])
                                
                            if (p == 4):
                                mat_dict[(i,j-1)][2][n_act[1]] =  float(split[2])                  
                                    
inv_dict = {}

for i in range(0,2):
    for j in range (0,9):
        inv_dict[(i,j)] = np.zeros(shape=(3,3))
        
        
with open('output.txt', 'w') as file:
     for i in range(0,2):
         for j in range (0,9):
             print("____________________________________________", file = file)
             print ("\n\n\nBIN   ",i, " ", j, file = file)
             print("Rich matrix:", file = file)
             print(np.transpose(mat_dict[(i,j)]), file = file)      
            
             print("\nInverse matrix:", file = file)
             
             if (np.linalg.det(mat_dict[(i,j)])>1e-10):
                  inv_dict[(i,j)] = np.linalg.inv(mat_dict[(i,j)])
                  print(inv_dict[(i,j)], file = file)     
             else:
                 print("MATRIX IS SINGULAR", file = file)
            
#             print("\nDeterminant", file = file)
#             print(np.linalg.det(mat_dict[(i,j)]), file = file)  

compare =True
tbin = 0
pbin = 0

inv_diff = {}

for i in range(0,2):
    for j in range (0,9):
        inv_diff[(i,j)] = np.zeros(shape=(3,3))
        
mat_diff = {}

for i in range(0,2):
    for j in range (0,9):
        mat_diff[(i,j)] = np.zeros(shape=(3,3))

mat_dav = {}

for i in range(0,2):
    for j in range (0,9):
        mat_dav[(i,j)] = np.zeros(shape=(3,3))
        
inv_dav = {}

for i in range(0,2):
    for j in range (0,9):
        inv_dav[(i,j)] = np.zeros(shape=(3,3))


if compare == True:
    with open('rich_inv.txt', 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
        
        for k in range(len(lines)):
            line = lines[k]
            
            if ('#' in line and k > 0):
                pbin += 1
                
                if (pbin == 8):
                    pbin = 0
                    tbin += 1
            
            if (tbin == 3 and pbin == 0):
                break
            
            if (tbin != 3 and np.linalg.det(mat_dict[(tbin,pbin)]) < 0.001):
                print("NULL DETERMINANT   ", tbin, "   ", pbin)
                continue
            
            split = line.split()
            
            if ("Rich" in line):
               print("\n\n\n",lines[k-1])
               print(line)
               for j in range(0,3):
                    split = lines[k+j+1].split()
    
                    if (len(split) == 3):
                        for i in range(0,3):
                            #print(split[i], "    ", (mat_dict[(tbin,pbin)][i][j]) ,"    ",float(split[i])-(mat_dict[(tbin,pbin)][i][j]))
                            mat_diff[(tbin,pbin)][i][j] = abs(float(split[i])-(mat_dict[(tbin,pbin)][i][j]))
                            mat_dav[(tbin,pbin)][i][j] = float(split[i])
                            if (abs(float(split[i])-(mat_dict[(tbin,pbin)][i][j])) > 0.01):
                                print(tbin," ", pbin, " ", i, " ", j, " ",abs(float(split[i])-(mat_dict[(tbin,pbin)][i][j])))
                        
                                
            if ("Inverse" in line):
               print("\n\n\n", line)
               for j in range(0,3):
                    split = lines[k+j+1].split()
    
                    if (len(split) == 3):
                        for i in range(0,3):
                            #♦print(split[i], "    ", (inv_dict[(tbin,pbin)][i][j]) ,"    ",float(split[i])-(inv_dict[(tbin,pbin)][i][j]))
                            inv_diff[(tbin,pbin)][i][j] = abs(float(split[i])-(inv_dict[(tbin,pbin)][i][j]))
                            inv_dav[(tbin,pbin)][i][j] = float(split[i])
                            # if (abs(float(split[i])-(inv_dict[(tbin,pbin)][i][j])) > 0.01):
                            #     print(tbin," ", pbin, " ", i, " ", j, " ",abs(float(split[i])-inv_dict[(tbin,pbin)][i][j]))

with open('output.txt', 'w') as file:
    for i in range(0,2):
        for j in range (0,9):
            
            if (i==2 and j == 7 ):
                continue
            
            print("____________________________________________", file = file)
            print ("\nBIN   ",i, " ", j,"\n", file = file)
            print("Rich matrix differences:\n", file = file)
            
            print("\nMy matrix:\n",mat_dict[(i,j)],"\n\n", file = file)
            
            print("\nDavide's matrix:\n",mat_dav[(i,j)],"\n\n", file = file)
            print("\nDifference:\n",file=file)
            print(mat_diff[(i,j)], file = file)      
            
            for s in range(0,2):
                for t in range (0,9):
                    if (mat_diff[(i,j)][s][t]>0.0001):
                        print("\nDifferent on [", s, ", ",t,"]",", the difference = ", mat_diff[(i,j)][s][t], file = file)
            
            print("\nInverse matrix differences:\n", file = file)
            
            print("\nMy matrix:\n",inv_dict[(i,j)],"\n\n", file = file)
            
            print("\nDavide's matrix:\n",inv_dav[(i,j)],"\n\n", file = file)
            print("\nDifference:\n",file=file)
            print(inv_diff[(i,j)], file = file)     
            
            for s in range(0,2):
                for t in range (0,9):
                    if (inv_diff[(i,j)][s][t]>1e-5):
                        print("\nDifferent on [", s, ", ",t,"]",", the difference = ", inv_diff[(i,j)][s][t], file = file)
            
print(abs(1.58876e-2-0.0158876))
    
    
