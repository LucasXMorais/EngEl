def isvogal(a, resp):
    if a == "a":
        resp[0] = resp[0] + 1
    if a == "e":
        resp[1] = resp[1] + 1
    if a == "i":
        resp[2] = resp[2] + 1
    if a == "o":
        resp[3] = resp[3] + 1
    if a == "u":
        resp[4] = resp[4] + 1
    return resp
string = str(input("Frase ou palavra = "))
string = string.lower()
vogais = [0 , 0 , 0 , 0 , 0]
espacos = 0
for seg in string:
    if any([seg == "a", seg == "e", seg == "i", seg == "o", seg == "u"]):
        vogais = isvogal(seg,vogais)
    if seg == " ":
        espacos = espacos + 1
print("A = ",vogais[0],"\nE = ",vogais[1],"\nI = ",vogais[2],"\nO = ",vogais[3],"\nU = ",vogais[4],"\nEspaços = ", espacos)        
print("A = ",vogais[0])
print("E = ",vogais[1])
