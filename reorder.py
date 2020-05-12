def reorder(array2n):
    n=5
    a_list=array2n[:n]
    b_list=array2n[n:2*n]
    c_list=[]
    for i in range(n):
        c_list.append(a_list[i])
        c_list.append(b_list[i])
    print(c_list) 
array2n=['a1','a2','a3','a4','a5','b1','b2','b3','b4','b5']
reorder(array2n)
