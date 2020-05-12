def reorder2(array2n):
    n=int(len(array2n)/2)
    for i in range(n):
        array2n.insert(2*i+1,array2n[2*i+n]) 
    array2n =  array2n[:2*n] 
    return array2n
