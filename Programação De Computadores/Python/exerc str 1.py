string1 = str(input("Palavar 1 = "))
string2 = str(input("Palavra 2 = "))
print("Tamanho da palavra 1 = ",len(string1))
print("Tamanho da palavra 2 = ",len(string2))
if len(string1) == len(string2):
    print("As duas tem o mesmo tamanho")
else:
    print("Têm tamanho diferente")
if string1 == string2:
    print("São iguais")
else:
    print("São diferentes")
