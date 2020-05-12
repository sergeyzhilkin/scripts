f = open('test','w')
for a in range(20000):
    for i in range(100):
        f.write(f'{i},')
    f.write('50\n')
f.close()        

