def calc(string_expression):
    fin_value=0
    value=0
    s=1 
    for i in string_expression:
        if i=='+':
            s=1
            fin_value+=value
            value=0
        elif i=='-':
            s=-1
            fin_value+=value
            value=0
        else:
            value*=10
            value+=int(i)*s
    fin_value+=value
    return fin_value

        
          
