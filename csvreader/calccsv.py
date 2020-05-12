import time
import concurrent.futures
import multiprocessing
def timedec(method):
    def timed(*args, **kwargs):
        start = time.time()
        result = method(*args, **kwargs)
        end = time.time()
        print('time spent for {} is {}'.format(method.__name__,end-start))
        return result
    return timed

def csv_sum_line(csv_line):
    final_line_sum = 0
    line_sum = 0
    for i in csv_line:
        if i.isnumeric():
            line_sum = line_sum*10 + int(i)
        else:
            final_line_sum += line_sum
            line_sum = 0
    return final_line_sum

#@timedec
def calccsv(n_first, n_last, fileaddress):
    with open(fileaddress,'r') as csv_file:
        n = 0
        csv_sum = 0
        for csv_line in csv_file:
            n+=1
            if n in range(n_first,n_last+1):
                csv_sum += csv_sum_line(csv_line)
    return csv_sum

@timedec
def multicalc(fileaddress,x):  #  x is a number of threads
    r = [] 
    a = []
    with open(fileaddress,'r') as csv_file:
        n = 0
        for i in csv_file:
            n+=1
    print('number of lines {}'.format(n))
    if x > n:
        x = n
    print('number of threads/processes: {}'.format(x))
    '''
    #  BLOCK FOR MULTI THREAD EXECUTION 
    with concurrent.futures.ThreadPoolExecutor(max_workers=x) as executor:
        for i in range(x): 
            r.append(executor.submit(calccsv,int(n*i/x) + 1,int(n*(i+1)/x),fileaddress).result())
    '''
    #  BLOCK FOR MULTIPROCESSING EXECUTION
    with multiprocessing.Pool() as pool:
        for i in range(x):
            a.append([int(n*i/x) + 1,int(n*(i+1)/x),fileaddress])
        r = pool.starmap(calccsv,a)
    return print('sum of all values in file {}: {}'.format(fileaddress,sum(r)))
     
