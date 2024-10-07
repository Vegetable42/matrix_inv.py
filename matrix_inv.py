import numpy as np


# Open the file in read mode
with open('rich_mat.txt', 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

n_act = (0,0)

mat_dict = {}

#initialization of the matrices
for i in range(0,2):
    for j in range (0,9):
        mat_dict[(i,j)] = np.zeros(shape=(3,3))

#loop for each line
for k in range(len(lines)):
    line = lines[k]

    #p is the 
    for p in range(0,5):
        if (p == 1 or p == 3): #if particle is pi+ or K+ we ignore it
            continue
        
        #to loop over all possible indices
        for q in range (0,3):
                #actual index
                n_act = (p,q)
                
                s = line.split()
                
                #this should be a condition for process identification
                #for this value we loop over i and j
                if (len(s) == 2 and int(s[0]) == n_act[0] and int(s[1]) == n_act[1]):
                                        
                    for i in range(0,2):
                        for j in range (1,10):
                            
                            #
                            split = lines[k+i*8+j].split()
                            
                            #basically zero values ignored
                            if (float(split[2]) < 1e-3):
                                continue
                            #actual value for pion-
                            if (p == 0):
                                mat_dict[(i,j-1)][0][n_act[1]] =  float(split[2])
                            #actual value for K-
                            if (p == 2):
                                mat_dict[(i,j-1)][1][n_act[1]] =  float(split[2])
                            #actual value for p
                            if (p == 4):
                                mat_dict[(i,j-1)][2][n_act[1]] =  float(split[2])                  
                                    
inv_dict = {}

for i in range(0,2):
    for j in range (0,9):
        inv_dict[(i,j)] = np.zeros(shape=(3,3))
        
        
with open('output.txt', 'w') as file:
     for i in range(0,2):
         for j in range (0,9):
             #print("____________________________________________", file = file)
             print ("BIN ",i, " ", j, file = file)
             #print("Rich matrix:", file = file)
             #print(np.transpose(mat_dict[(i,j)]), file = file)      
            
             #print("Inverse matrix:", file = file)
             
             if (np.linalg.det(mat_dict[(i,j)])>1e-10):
                  inv_dict[(i,j)] = np.linalg.inv(mat_dict[(i,j)])
                  #print(np.transpose(inv_dict[(i,j)]), file = file)   
                  for s in range(0,3):
                          m = 0;
                          print(inv_dict[(i,j)][m, s], " ", inv_dict[(i,j)][m+1, s], " ", inv_dict[(i,j)][m+2, s], file = file)
             else:
                 print("MATRIX IS SINGULAR", file = file)
            
#             print("\nDeterminant", file = file)
#             print(np.linalg.det(mat_dict[(i,j)]), file = file)  

compare = True
tbin = 0
pbin = 0

inv_diff = {}
mat_diff = {}
inv_dav = {}
mat_dav = {}

for i in range(0,2):
    for j in range (0,9):
        inv_diff[(i,j)] = np.zeros(shape=(3,3))
        inv_dav[(i,j)] = np.zeros(shape=(3,3))
        mat_diff[(i,j)] = np.zeros(shape=(3,3))
        mat_dav[(i,j)] = np.zeros(shape=(3,3))
        
#Comparison of mine and Davides values
if compare == True:
    with open('rich_inv.txt', 'r') as file:
        # Read all lines from the file
        lines = file.readlines()
        
        for k in range(len(lines)):
            line = lines[k]
            
            if ('#' in line and k > 0):
                pbin += 1
                
            #number of pbins reached
            if (pbin == 9):
                pbin = 0
                tbin += 1
            
            if (tbin == 2 and pbin == 0):
                break
            
            if (tbin != 2 and np.linalg.det(mat_dict[(tbin,pbin)]) < 0.001):
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

# with open('output.txt', 'w') as file:
#     for i in range(0,2):
#         for j in range (0,9):
#             print("AAAAAAa", file = file)
#             if (i==2 and j == 7 ):
#                 continue
            
#             print("____________________________________________", file = file)
#             print ("\nBIN   ",i, " ", j,"\n", file = file)
#             print("Rich matrix differences:\n", file = file)
            
#             print("\nMy matrix:\n",mat_dict[(i,j)],"\n\n", file = file)
            
#             print("\nDavide's matrix:\n",mat_dav[(i,j)],"\n\n", file = file)
#             print("\nDifference:\n",file=file)
#             print(mat_diff[(i,j)], file = file)      
            
#             for s in range(0,2):
#                 for t in range (0,9):
#                     if (mat_diff[(i,j)][s][t]>0.0001):
#                         print("\nDifferent on [", s, ", ",t,"]",", the difference = ", mat_diff[(i,j)][s][t], file = file)
            
#             print("\nInverse matrix differences:\n", file = file)
            
#             print("\nMy matrix:\n",inv_dict[(i,j)],"\n\n", file = file)
            
#             print("\nDavide's matrix:\n",inv_dav[(i,j)],"\n\n", file = file)
#             print("\nDifference:\n",file=file)
#             print(inv_diff[(i,j)], file = file)     
            
#             for s in range(0,2):
#                 for t in range (0,9):
#                     if (inv_diff[(i,j)][s][t]>1e-5):
#                         print("\nDifferent on [", s, ", ",t,"]",", the difference = ", inv_diff[(i,j)][s][t], file = file)
            

with open ('counts.txt', 'r') as file:
    
    counts_plus = {}
    counts_minus = {}
    actual = "p+"
    for i in range(0,2):
        for j in range (0,9):
            counts_plus[(i,j)] = np.zeros(3)
            counts_minus[(i,j)] = np.zeros(3)

    # Read all lines from the file
    lines = file.readlines()
    for k in range(len(lines)):
        line = lines[k]
        
        s = line.split()
        
        
        if (len(s) == 1):
            print(s)
            if (s[0] == "p+"):
                actual = s[0]
            if (s[0] == "p-"):
                actual = s[0]                
            if (s[0] == "k+"):
                actual = s[0] 
            if (s[0] == "k-"):
                actual = s[0]
            if (s[0] == "pi+"):
                actual = s[0]
            if (s[0] == "pi-"):
                actual = s[0]
        
        elif (len(s) == 3):
            theta_bin = float(s[0])
            p_bin = float(s[1])
            
            if (actual == "pi+"):
                counts_plus[(theta_bin, p_bin)][0] = float(s[2])
                
            elif (actual == "k+"):
                counts_plus[(theta_bin, p_bin)][1] = float(s[2])
                
            elif (actual == "p+"):
                counts_plus[(theta_bin, p_bin)][2] = float(s[2])
                           
            elif (actual == "pi-"):
                counts_minus[(theta_bin, p_bin)][0] = float(s[2])
                
            elif (actual == "k-"):
                counts_minus[(theta_bin, p_bin)][1] = float(s[2])
                
            elif (actual == "p-"):
                counts_minus[(theta_bin, p_bin)][2] = float(s[2])
            
    print(counts_plus)
    print(counts_minus)        
    
    
with open('multiplication.txt', 'w') as file:
    result_plus = {}
    result_minus = {}
    
    for i in range(0,2):
        for j in range (0,9):      
            
            print(i," ",j, file=file)
            print("PLUS", file = file)
            print (np.matmul(np.transpose(inv_dict[(i,j)]), counts_plus[(i,j)]), file = file)
            
            print("MINUS", file = file)
            print (np.matmul(np.transpose(inv_dict[(i,j)]), counts_minus[(i,j)]), file = file)
            print(file=file)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
