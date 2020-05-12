from collections import deque
def sminstr(mystring):
    init_index=0
    a='none'
    queue=deque() 
    while init_index < len(mystring):
        print(init_index, mystring[init_index])
        if mystring[init_index]== '+' or  mystring[init_index] == '-':
            a = mystring[init_index] 
        elif mystring[init_index] == '(':
            start=init_index
            num=1
            while num !=0:
                init_index+=1
                if mystring[init_index] == '(':
                    num+=1
                if mystring[init_index] == ')':
                    num-=1
            queue.extend(sminstr(mystring[start+1:init_index]))
            if a != 'none':
                queue.append(a)
        else:
            queue.append(mystring[init_index])
            if a != 'none':
                queue.append(a)
        init_index+=1
    return queue
