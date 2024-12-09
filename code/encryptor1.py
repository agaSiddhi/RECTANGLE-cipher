sbox= [0x6, 0x5, 0xc, 0xa, 0x1, 0xe, 0x7, 0x9, 0xb, 0x0, 0x3, 0xd, 0x8, 0xf, 0x4, 0x2]
sboxinv=[0x9,0x4, 0xf, 0xa, 0xe, 0x1, 0x0, 0x6, 0xc, 0x7, 0x3, 0x8, 0x2, 0xb, 0x5, 0xd]
rcon= [0x01, 0x02, 0x04, 0x09, 0x12, 0x05, 0x0B, 0x16, 0x0C, 0x19, 0x13, 0x07, 0x0F, 0x1F, 0x1E, 0x1C, 0x18, 0x11, 0x03, 0x06, 0x0D, 0x1B, 0x17, 0x0E, 0x1D]
import random

allkeys=[]

def tilda(bn):
    sr=""
    for i in bn:
        if(i=='0'):
            sr+='1'
        else:
            sr+='0'
    return sr

def keyupdate(key,round):
    # print("Before Sb",key)
    for i in range(0,4):
        # print(key[i])
        l1=key[i][-1]
        l2=key[i][-2]
        l3=key[i][-3]
        l4=key[i][-4]

        num = int(l1)+int(l2)*2 + int(l3)*4 + int(l4)*8
        sbb = sbox[num]
        t = bin(sbb).replace("0b","")

        x = '0'*(4-len(t))+t
        temp = key[i][:-4]
        key[i] = temp+x
        # print(key)


    # print("The current",key)
    temp=key[0]
    res=bin(((int(key[0],2)>>8) | (int(key[0],2)<<8)) ^ int(key[1],2)).replace("0b","")
    key[0]='0'*(16-len(res))+res
    key[0]=key[0][-16:]
    key[1]=key[2]
    key[2]=key[3]
    res=bin( ( (int(key[3],2)>>4) | (int(key[3],2) <<12))^int(key[4],2) ).replace("0b","")
    key[3]='0'*(16-len(res))+res
    key[3]=key[3][-16:]
    key[4]=temp
    res=bin( int(key[0],2) ^ rcon[round] ).replace("0b","")
    key[0]='0'*(16-len(res))+res
    key[0]=key[0][-16:]


    # print("The current",key)
    temp=key[0]
    res=bin(((int(key[0],2)>>8) | (int(key[0],2)<<8)) ^ int(key[1],2)).replace("0b","")
    key[0]='0'*(16-len(res))+res
    key[0]=key[0][-16:]
    key[1]=key[2]
    key[2]=key[3]
    res=bin( ( (int(key[3],2)>>4) | (int(key[3],2) <<12))^int(key[4],2) ).replace("0b","")
    key[3]='0'*(16-len(res))+res
    key[3]=key[3][-16:]
    key[4]=temp
    res=bin( int(key[0],2) ^ rcon[round] ).replace("0b","")
    key[0]='0'*(16-len(res))+res
    key[0]=key[0][-16:]



def addroundkey(state,key):
    for i in range(0,4):
        state[i]=bin(int(state[i],2)^int(key[i],2)).replace("0b","")
        state[i]='0'*(16-len(state[i]))+state[i]
        state[i]=state[i][-16:]


def subcolumn(state):
    temp0=[[],[],[],[]]
    for a1 in range(4):
        for a2 in range(16):
            temp0[a1].append(0)
    for i in range(16):
        l1=state[0][i]
        l2 = state[1][i]
        l3 = state[2][i]
        l4 = state[3][i]


        num = int(l1)+int(l2)*2 + int(l3)*4 + int(l4)*8
        sbb= sbox[num]

        t = bin(sbb).replace("0b","")

        x = '0'*(4-len(t))+t

        temp0[0][i] = x[-1]
        temp0[1][i] = x[-2]
        temp0[2][i] = x[-3]
        temp0[3][i] = x[-4]

    todo=["","","",""]
    for b in range(4):
        l=""
        for q in range(16):
            l+=temp0[b][q]
        todo[b]=l

    state = todo
    return state

def shiftrows(state):
    shift=[0,1,12,13]
    for i in range(1,4):
        temp=(int(state[i],2)<<shift[i])|(int(state[i],2)>>(16-shift[i]))
        state[i]=bin(temp).replace("0b","")
        state[i]='0'*(16-len(state[i]))+state[i]
        state[i]=state[i][-16:]

def encrypt(state,key):
    print("Starting state is:",state)
    print("starting with the key:", key)
    for j in range (0,25):
        print("Round :",j)

        addroundkey(state,key)
        print("after adding key",state)
        print("added key",key)
        # print("beforeee",state)
        state = subcolumn(state)
        print("after sbox",state)
        # print("afterrr",state)
        shiftrows(state)
        print("after shift",state)
        # print(state)
        keyupdate(key , j)
        # print("-----------------------------------------\n")
        print(state)
        # print("key")
        # print(key)
        print("-----------------------------------------\n")

    addroundkey(state,key)
    print("FINAL STATE")
    print(state)


    finalstring = ""

    for i in range(4):
        finalstring+=state[i][::-1]

    print("hexform of cipher is:",hex(int(finalstring,2))[2:])


def encryption():

    str=input("Enter the message in hex form: ")
    while(len(str)>16):
        print("Incorrect Message Enter again")
        str=input("Enter the message in hex form: ")
    while(len(str)!=16):
        str+='0'
    state=[]
    temp=""
    for i in range(len(str)):
        res=int(str[i],16)
        bn=bin(res).replace("0b","")
        bn='0'*(4-len(bn))+bn
        temp+=bn
        if((i%4)==3):
            state.append(temp[::-1])
            temp=""

    # generate a random key
    x="0123456789abcdef"

    k=""

    for i in range(20):
        ind = random.randint(0,15)
        k+=x[ind]

    temp=""
    print("encrypting with the key,",k)
    print()
    key=[]
    for i in range(len(k)):
        res=int(k[i],16)
        bn=bin(res).replace("0b","")
        bn='0'*(4-len(bn))+bn
        temp+=bn
        if((i%4)==3):
            key.append(temp[::-1])
            temp=""
    # print(state)
    # print(key)
    encrypt(state,key)

encryption()

# aa123ef000000000
# fe46ece954aeb336d683