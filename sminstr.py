from collections import deque

# expressions when like (-1) or (-2)
def sminstr(mystring):
    init_index = 0
    a = 'none'
    queue = deque()
    value = 0
    s = 0
    while init_index < len(mystring):
        if mystring[init_index] == '+' or mystring[init_index] == '-':
            if init_index >0 and mystring[init_index-1] != ')' :
                if s == -1:
                    value = value*(-1)
                queue.appendleft(value)
                if a != 'none':
                    queue.appendleft(a)
            value = 0
            s = 0
            a = mystring[init_index]  # save sign to append after next value or brackets
        elif mystring[init_index] == '(': # find start and end indices of segment in brackets and make recursive call to it:
            start = init_index
            num = 1
            while num != 0:
                init_index += 1
                if mystring[init_index] == '(':
                    num += 1
                if mystring[init_index] == ')':
                    num -= 1
            inner_queue = sminstr(mystring[start + 1:init_index])
            inner_queue.reverse()  # need to reverse because of crazy behavior of extendleft
            queue.extendleft(inner_queue)
            if a != 'none':
                queue.appendleft(a)  # append sign that was before (...)
        else:
            if init_index == 1:
                if a == '-':  # it's just a negative number
                    s = -1  # queue.appendleft(int(mystring[init_index])*(-1))
                elif a == '+':  # it's just a positive number
                    s = 1  # queue.appendleft(int(mystring[init_index]))
                a = 'none'
            value *= 10
            value += int(mystring[init_index])  # queue.appendleft(int(mystring[init_index]))
        if init_index == len(mystring)-1 and mystring[init_index] != ')':
            if s == -1:
                value = value * (-1)
            queue.appendleft(value)
            if a != 'none':
                queue.appendleft(a)
        init_index += 1
    return queue
