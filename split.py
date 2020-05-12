def split(istring, separator=''):
    listOfSubstrings=[]
    substring=''
    for i in range(0,len(istring)):
        if istring[i] == separator:
            listOfSubstrings.append(substring)
            substring=''
        else:
            substring+= istring[i]
    listOfSubstrings.append(substring)
    return listOfSubstrings    
     
