def movImm(op,reg,temp,ins,t):
    t+=op["mov"]+"0"
    #//print(reg)
    t+=reg[temp[ins].split()[1]]
    regval[temp[ins].split()[1]]=temp[ins].split()[2][1:]
    while len(regval[temp[ins].split()[1]])!=16:
        regval[temp[ins].split()[1]]="0"+regval[temp[ins].split()[1]]
    im=bin(int(temp[ins].split()[2][1:]))[2:]
    while len(im)!=7:
        im="0"+im
    t+=im
    #//print(t+"\n")
    return t

def movReg(op,reg,temp,ins,t): 
    t+=op["mov"]+"00000" 
    t+=reg[temp[ins].split()[1]]
    t+=reg[temp[ins].split()[2]]
    regval[temp[ins].split()[1]]=regval[temp[ins].split()[2]]
    while len(regval[temp[ins].split()[1]])!=16:
        regval[temp[ins].split()[1]]="0"+regval[temp[ins].split()[1]]
    return t

def load(op,reg,temp,ins,t):
    if temp[ins].split()[2] in var.keys():
        while len(var[temp[ins].split()[2]])!=16:
            var[temp[ins].split()[2]]="0"+var[temp[ins].split()[2]]
        regval[temp[ins].split()[1]]=var[temp[ins].split()[2]]
    else :
        regval[temp[ins].split()[1]]="0000000000000000"
    t+=op["ld"]+"0"
    t+=reg[temp[ins].split()[1]]
    while len(mem[temp[ins].split()[2]])!=7:
        mem[temp[ins].split()[2]]="0"+mem[temp[ins].split()[2]]
    t+=mem[temp[ins].split()[2]]
    return t

def store(op,reg,temp,ins,t):
    var[temp[ins].split()[2]]=regval[temp[ins].split()[1]]
    t+=op["st"]+"0"
    t+=reg[temp[ins].split()[1]]
    while len(mem[temp[ins].split()[2]])!=7:
        mem[temp[ins].split()[2]]="0"+mem[temp[ins].split()[2]]
    t+=mem[temp[ins].split()[2]]
    return t

def multiply(op,reg,temp,ins,t):
    regval[temp[ins].split()[1]]=bin(int(regval[temp[ins].split()[2]],2)*int(regval[temp[ins].split()[3]],2))[2:]
    if len(regval[temp[ins].split()[1]])>16:
        q=int(regval["FLAGS"],2)
        regval["FLAGS"]=bin(q+1)[2:]
        temp=regval[temp[ins].split()[1]]
        regval[temp[ins].split()[1]]=""
        for i in range(len(temp)-16,len(temp),1):
            regval[temp[ins].split()[1]]+=temp[i]
    t+=op["mul"]+"00"
    t+=reg[temp[ins].split()[1]]+reg[temp[ins].split()[2]]+reg[temp[ins].split()[3]]
    return t

def divide(op,reg,temp,ins,t):
    if int(regval[temp[ins].split()[3]],2)==0:
        q=int(regval["FLAGS"],2)
        regval["FLAGS"]=bin(q+1)[2:]
        return None
    regval[temp[ins].split()[1]]=bin(int(regval[temp[ins].split()[2]],2)/int(regval[temp[ins].split()[3]],2))
    if len(regval[temp[ins].split()[1]])>16:
        q=int(regval["FLAGS"],2)
        regval["FLAGS"]=bin(q+1)[2:]
        temp=regval[temp[ins].split()[1]]
        regval[temp[ins].split()[1]]=""
        for i in range(len(temp)-16,len(temp),1):
            regval[temp[ins].split()[1]]+=temp[i]
    t+=op["div"]+"00"
    t+=reg[temp[ins].split()[1]]+reg[temp[ins].split()[2]]+reg[temp[ins].split()[3]]
    return t

def hlt(arr,dic):
    arr.append(dic["hlt"]+"00000000000")

op={"add":"00000","sub":"00001","mov":"00010","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
regval={"R0":"0000000000000000","R1":"0000000000000000","R2":"0000000000000000","R3":"0000000000000000","R4":"0000000000000000","R5":"0000000000000000","R6":"0000000000000000","FLAGS":"0000000000000000"}
var={}
mem={}
labels={}
f=open("C://Users//ABCD//OneDrive//Desktop//c-training//.vscode//test1.txt","r")
lines=[]
addresses={}
for line in f.readlines():
    if line.strip()!="":
        lines.append(line.strip())
f.close()
i=0
for line in lines:
    index=bin(i)[2:]
    #print(index)
    while (len(index)!=7):
        index="0"+index
    if line.split()[0]!="var":
        addresses[index]=line
        #print(addresses)
        i+=1
for line in lines:
    index=bin(i)[2:]
    while (len(index)!=7):
        index="0"+index
    if line.split()[0]!="var":
        break
    addresses[index]=line
    i+=1
    #print(addresses)
for i,j in addresses.items():
    if j.split()[0]=="var":
        mem[j.split()[1]]=i
    if ":" in j:
        labels[j.split()[0][:-1]]=i
# print(addresses)
# print(mem)
# print(labels)
temp=[]
f=open("C://Users//ABCD//OneDrive//Desktop//c-training//.vscode//test1.txt","r")
for line in f.readlines():
    if line.strip()!="" and line.strip().split()[0]!="var":
        temp.append(line.strip())
f.close()
ans=[]
pc="0000000"
while (addresses[pc].split()[-1])!="hlt":
    ins=int(pc,2)
    t=""
    if temp[ins].split()[0]=="mov" and temp[ins].split()[-1][0]=="$":
       t=movImm(op,reg,temp,ins,t) 
    elif temp[ins].split()[0]=="mov" and temp[ins].split()[-1][0]=="R":
        t=movReg(op,reg,temp,ins,t)
    elif temp[ins].split()[0]=="ld":
        t=load(op,reg,temp,ins,t)
    elif temp[ins].split()[0]=="st":
        t=store(op,reg,temp,ins,t)
    elif temp[ins].split()[0]=="mul":
        t=multiply(op,reg,temp,ins,t)
    elif temp[ins].split()[0]=="div":
        t=divide(op,reg,temp,ins,t)
    ans.append(t)
    pc=bin(ins+1)[2:]
    while (len(pc)!=7):
        pc="0"+pc
hlt(ans,op)
for i in ans:
    print(i)
