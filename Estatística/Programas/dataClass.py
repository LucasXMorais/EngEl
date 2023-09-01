import numpy as np

class Data:
    def __init__(self, data):
        auxData = [data]
        running = True
        
        while running:                        
            auxSort = []                        
            for i in range(len(auxData)): 
                if len(auxData[i]) > 1:  
                    less = []
                    greater = []
                    
                    for j in range(len(auxData[i])-1):
                        if auxData[i][j] <= auxData[i][-1]: 
                            less.append(auxData[i][j])
                        else:
                            greater.append(auxData[i][j]) 
                            
                    greater = [auxData[i][-1]] + greater
            
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
            
        self.data = result
    
        media = 0
        for i in range(len(self.data)):
            media += self.data[i]
        self.avg = media/len(self.data)

        var = 0
        for i in range(len(self.data)):
            var += (self.data[i] - self.avg)**2
        self.vrc = var/len(self.data)

        self.desvioPad = (self.vrc)**(1/2)

        self.coefVar = (self.desvioPad/self.avg)*100
        
    def show(self):
        print(self.data)
        print("média:",self.avg)
        print("variânica:",self.vrc)
        print("desvio padrão:",self.desvioPad)
        print("coeficiente de variância:",self.coefVar)
        
    def perc(self,quantil):
        quantil = abs(quantil)
        if quantil<=1:
            pos = quantil*(len(self.data)+1)
            if pos % 1 == 0:
                print(quantil*100," percentil:",self.data[int(pos)-1])
            else:
                print(quantil*100," percentil:",(self.data[int(np.floor(pos))-1]+self.data[int(np.ceil(pos))-1])/2)
                
    def moda(self):
        freq = [{
                "Area": self.data[0],
                "Freq": 0
            }]
        modasAux = 0
        for i in range(len(self.data)):
            if freq[-1]["Area"] == self.data[i]:
                 modasAux+=1
                 if i == len(self.data)-1:
                    freq[-1]["Freq"] = modasAux
            else:
                freq[-1]["Freq"] = modasAux
                freq.append({
                    "Area": self.data[i],
                    "Freq": 1
                })
                modasAux = 1
  
        modas = [freq[0]]
        for i in range(len(freq)):
            if freq[i]["Freq"] == modas[0]["Freq"] and freq[i]["Area"] != modas[0]["Area"]:
                modas.append(freq[i])
            elif freq[i]["Freq"] > modas[0]["Freq"]:
                modas = [freq[i]]
        
        print(freq)
        print(modas)
        
d = Data([27.8,28.3,27.1,26.5,27.7,28.3,27.7,28.1,26.6,27.3,27.4,26.5,29.2,28.8,29.4,27.8,26.3,27.6,29.3,28.6,26.9,30.0,30.9,27.4,26.6,27.5,28.0,27.8,27.1,28.4,28.3,27.6,26.8,27.0,28.6,27.6,28.2,28.9,28.3,27.9,27.0,27.9,27.7,25.6,30.4,27.5,29.5,28.9,29.0,29.0,29.7,28.5,29.7,28.2,27.9,29.3,29.5,28.0,28.9,28.3,26.0,25.6,30.1,28.2,28.8,27.2,27.5,29.0,28.5,27.7,29.3,27.9,27.9,27.9,29.3,27.6,23.2,23.0,22.9,22.0,24.1,22.9,22.4,23.0,24.6,22.3,25.0,22.9,23.8,22.4,21.7,24.5,24.1,23.9,22.5,23.9,23.1,22.2,23.5,23.7,21.5,21.2,22.8,21.8,22.7,24.7,24.3,22.5,24.1,23.7,23.1,24.2,23.6,23.9,24.1,22.5,21.5,23.7,23.4,24.6,23.3,22.7,23.9,22.5,22.5,23.2,23.3,22.8,23.1,23.1,23.2,22.8,22.0,22.9,23.4,23.9,23.3,22.7,23.5,23.6,22.5,20.9,22.5,22.8,22.3,23.6,22.8,23.5,24.1,24.1,23.0,22.7])

print(len(d.data))
d.show()
d.perc(0.5)
d.moda()


