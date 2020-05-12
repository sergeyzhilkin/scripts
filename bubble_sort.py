def minimum(inlist):
 minvalue=inlist[0]
 minindex=0
 for i in range(1,len(inlist)):
  if minvalue>=inlist[i]:
   minvalue=inlist[i]
   minindex=i
 return  (minvalue,minindex)

def bubble_sort(initlist):
 for i in range(0,len(initlist)):
  minvalue,minindex = minimum(initlist[i:])
  print(minvalue,minindex)
  print(initlist[i:])
  initlist[minindex+i]=initlist[i]
  initlist[i]=minvalue
  

initlist = [3,7,2,6]

 
