def recursion(init_list,i=0):
    if i == int(len(init_list)/2): 
    #    print(init_list)
        return init_list
    init_list[i],init_list[-i-1] = init_list[-i-1], init_list[i]    
    recursion(init_list,i+1)
