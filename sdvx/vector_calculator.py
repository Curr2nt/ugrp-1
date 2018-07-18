
#I. Check L or R
"""
1. basically, Left side including knob-L and BT 1,2 and FX-L are 'L'
and totally same at the other side but 'R'
2. all is L when knob-R is activated except "stay knob", vice versa.
3-1. a.k.a. particular hand position: "hand-crossing(손교차)'
->only when one of knob is "stay"
3-2.'more easy hand position if one use his or her "technical skill"
(기교를 써서 더 쉬운 손배치가 가능한 경우 -> HEAVENLY SMILE MXM)' 
"""

#duplicated code start
import sys
import re

fileobj=open(sys.argv[1],'rt', encoding='UTF8')
file_content=fileobj.read()
fileobj.close()

#split files
#print(file_content)
#print()
c_info=[]
c_cont_all=[]
c_cont=[]
lsplit=re.split('\n+',file_content)
for i in range(len(lsplit)):
    if (lsplit[i]=='--'):
        c_info=lsplit[:i] #0~i-1
        c_cont_all=lsplit[(i+1):] # i+1 ~ end
        break
#print("chart info:")
#print(c_info)
#print("chart content:")
#print(c_cont_all[:10])

c_cont.append([])
tune=0
for i in range(len(c_cont_all)):
    if(c_cont_all[i]!='--'):
        c_cont[tune].append(c_cont_all[i])
    else: #new tune
        c_cont.append([])
        tune+=1
#print(c_cont[2])
#print("tune:", tune)


#print(c_cont[2])
#print(c_cont[2][0])
#print(c_cont[2][0][0])
#format: c_cont[#no. tune] #len(c_cont[tune])= 1+1 or 4 or 8+1, ...
notelist=[]
infolist=[]
for i in range(tune):
    infolist.append([])
    noteline=len(c_cont[i])
    #print(c_cont[i])
    #print("noteline:", noteline)
    for j in range(len(c_cont[i])):
        if(c_cont[i][j][0] not in ['0','1','2']):
            infolist[i].append(j)
            noteline-=1 
    #print("i:",i,"noteline:", noteline)
    notelist.append(noteline)
#print(infolist)

#duplicated code end 
#3.(심화): 주차가 2개의 소마디 이상으로 진행되면 '조작없음'으로 판단. or 그냥 주차는 조작없음으로.

#현재 라인에 노브가 있는지 확인.
#칩노트: 결과적으로 노브가 무조건 우선시.
#노브없으면 기본값으로 배정 (현재 기교 무시)
#노브있으면, 노브의 반댓손으로 처리.

#홀드노트: 기존에 있는 걸 우선시함.
#동시에 나올 경우 노브 > 홀드 > 칩. 노브와 홀드가 동시에 같은 손으로 처리되지 않는것을 원칙으로 한다. (counting)
#노브있으나 홀드on이면 홀드 손 유지. 노브를 반대손으로 처리
#노브있으나 홀드off이면 노브 손 기본값, 홀드를 반대손으로 처리
#한번 홀드on하면 끝날때까지 손을 바꾸지 않음.

holdon=[0]*6 #check if the hold is already on(active)
holdside=['N']*6 #L/R: Left/Right   B:Both; also granted when other hand is free N:Nullity; something went wrong
knobon=0 #check if the knob is already on(active)
#knobon=[0]*2 
knobside='N'
BTFX=[0,1,2,3,5,6]
KNOB=[8,9]

#BTFX, KNOB: hand-wise
#holdon, holdside: numeric-wise

def otherside(hand, side):
    if side=='L':
        return 'R'
    if side=='R':
        return 'L'
    if side=='B':
        if hand in [0,1,5,8]:
            return 'R'
        if hand in [2,3,6,9]:
            return 'L' 
    if side=='N':
        return 'N'

def side(hand):
    if hand in [0,1,5,8]:
        return 'L'
    if hand in [2,3,6,9]:
        return 'R'

def check_code(mode, hand):
    if (mode=='chip'):
        if hand in [0,1,2,3]:
            return '1'
        if hand in [5,6]:
            return '2'
    if (mode=='hold'):
        if hand in [0,1,2,3]:
            return '2'
        if hand in [5,6]:
            return '1'

f2=open("./ksh/directed_"+sys.argv[1].replace('./ksh/',''),"w",encoding="UTF8")
f2.write('\n'.join(c_info)+'\n')

for i in range(34,tune): #i: number of tunes
    f2.write("#"+str(i)+'-------\n')
    for j in range(notelist[i]+len(infolist[i])): #j: number of lines in a tune
        if(j not in infolist[i]): #c_cont[i][j]: 1111|00|--
            listline=list(c_cont[i][j])
            #check the switches
            if(any([holdon[x] for x in range(6)])):
                for k in range(len(BTFX)):
                    if listline[BTFX[k]]!=check_code('hold',BTFX[k]):
                        holdon[k]=0
                        holdside[k]='N'
            if(knobon):
                if(all([listline[x] in ['-',':'] for x in KNOB])):
                    #print(j,"knobon off")
                    knobon=0
                    knobside='N'
            #scan one line: 1111|00|--
            #print('@while_start', j, holdside, holdon)
            hand=8
            while(hand!=7):
                if(hand in KNOB):
                    if (listline[hand] not in ['-',':']):
                        for k in range(6):
                            if holdon[k]:
                                listline[hand]=otherside(BTFX[k], holdside[k])
                                break
                        else:
                            listline[hand]=side(hand)
                        knobon=1
                        knobside=listline[hand]
                    else:
                        listline[hand]=' '
                if(hand in BTFX):
                    if (listline[hand]!='0'):
                        if(listline[hand]==check_code('chip', hand)):
                            if(knobon):
                                listline[hand]=otherside(hand, knobside)
                            else:
                                listline[hand]=side(hand)
                        elif(listline[hand]==check_code('hold', hand)):
                            if(knobon):
                                listline[hand]=otherside(hand, knobside)
                            else:
                                for x in KNOB:
                                    if(listline[x] not in ['-',':',' ']): #if(listline[8]!=' '):
                                        #print(hand, 'knob')
                                        listline[hand]=otherside(x,side(x))
                                else:
                                    if(holdon[BTFX.index(hand)]):
                                        #print(hand, 'holdon')
                                        listline[hand]=holdside[BTFX.index(hand)]
                                    else:
                                        #print(hand, 'side')
                                        #print(BTFX.index(hand), 'side')
                                        #print(holdon[BTFX.index(hand)]==1)
                                        listline[hand]=side(hand)
                            holdon[BTFX.index(hand)]=1
                            holdside[BTFX.index(hand)]=listline[hand]
                    else:
                        listline[hand]=' '
                hand+=1
                if hand==10:
                    hand=0
            #print('@while_end  ', j, holdside, holdon)
            f2.writelines(''.join(listline)+'\n')
        else:
            f2.write(c_cont[i][j]+'\n')
f2.close()