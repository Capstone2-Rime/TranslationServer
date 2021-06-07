import hgtk

loc="/home/ubuntu/workspace/demo/dataset/afterset.txt"
f = open(loc,'r', encoding='utf-8')
line=f.read()
data=[]

ls=line.split(',')
for i in ls:
    if(hgtk.checker.is_hangul(i.strip())):
        data.append(i.strip())
        print(data[-1])
