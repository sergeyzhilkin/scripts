def uper(strng):
    upper_strng=''
    for i in strng:
        upper_i=i
        if i.isalpha():
            if ord(i) > 90:
                upper_i = chr(ord(i)-32)
        upper_strng+=upper_i    
    return upper_strng    
