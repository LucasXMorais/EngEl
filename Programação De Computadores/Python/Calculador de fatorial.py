fim = False
while fim == False:
    n = int(input("N! = "))
    if n == 0 or n == 1:
        print("N! =", 1)
    if n > 1:
        nf = 1
        for c in range(1, n):
            nf = nf * c
        print("N! =",nf)
    if n < 0:
        print("Invalid!!")
        
    
