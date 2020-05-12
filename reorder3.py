def reorder3(array2n):
    n = int(len(array2n)/2)
    for i in range(n):
        array2n.append(array2n[i])
        array2n.append(array2n[n+i])
    print(array2n[2*n:])
    
