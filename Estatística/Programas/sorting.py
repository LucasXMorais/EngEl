import numpy as np

#data = [4,1,8,9,3,2,1,4]
#data = [44,51,11,90,76,36,64,37,43,72,53,62,36,74,51,72,37,28,38,61,47,63,36,41,22,37,51,46,85,13]
#data = [28,25,21,15,7,14,9,27,21,24,14,17,16]
#data = [3,4,5,6,7]
data = [2,7,1,3,1,2,8,9,9,2,5,4,7,3,7,5,4,7,2,3,5,5,9,5,6,3,9,3,4,9,8,8,2,3,9,5]
# data = [34,43,31,37,24,25,27,22,21,26]
# data = [2300,2500,1800,1800,1500,1500,1500,1350,1020,1020]
# data = [5,8,6,8,3,2,5,2,3,3]
#data = [15,15,15,15,15,15,25,25,35,35,35,35,35,35,35,45,45,45,45,45]

def sort(data):
    
    less = []
    greater = []
    
    for i in range(len(data)-1):
        if data[i] <= data[-1]: 
            less.append(data[i])
        else:
            greater.append(data[i]) 
            
    greater = [data[-1]] + greater
            
    return less, greater

auxData = [data]
running = True
while running:
    
    auxSort = []
    
    for i in range(len(auxData)):   
        if len(auxData[i]) > 1:  
            less = []
            greater = []
            less, greater = sort(auxData[i]) 
            if len(less)!=0:auxSort.append(less)
            if len(greater)!=0:auxSort.append(greater)  
        else: 
            auxSort.append(auxData[i])
            
    auxData = auxSort
    
    if len(auxData) == len(data):
        running = False
        
result = []
for i in range(len(auxData)):
    result.append(auxData[i][0])
        
print("result:",result)
print("result size:",len(result))

