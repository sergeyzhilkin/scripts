def printarg(*anyargs):
    if anyargs:
        if len(anyargs)==1:
            print(anyargs[0])
        else:
            print(anyargs[0],anyargs[len(anyargs)-1])
 
