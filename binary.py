def binary(a,sorted_list,first_i=0):
    if a not in sorted_list:
        return -1
    else:
        middle_i = int(len(sorted_list)/2)-1
        if middle_i == 0:
            for i in range(len(sorted_list)):
                if sorted_list[i] == a:
                    return print(first_i +i)
                    #return
        if sorted_list[middle_i] == a:
            return print(first_i+ middle_i)
            #return
        if sorted_list[middle_i] > a:
            binary(a,sorted_list[:middle_i],first_i)
        if sorted_list[middle_i] < a:
            binary(a,sorted_list[middle_i+1:],first_i + middle_i + 1 )
