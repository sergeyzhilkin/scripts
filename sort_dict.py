def sortdict(dict):
 sort_val_list =[]
 for n in dict:
  sort_val_list.append(dict[n])
 sort_val_list.sort()
 #print(sort_val_list)
unsorted_dict = {"item2":4,"item1":2,"item4":13,"item3":7,"item5":29}
for i in unsorted_dict:
 print(unsorted_dict[i].sort())
#sortdict(unsorted_dict)
