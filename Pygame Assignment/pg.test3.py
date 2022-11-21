l=[3,6,1,0,2,4]
l = [(l[i], i) for i in range(len(l))]
l.sort(key=lambda x: x[0])
print(l)