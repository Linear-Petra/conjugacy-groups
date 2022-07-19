########
#
# Lynn & Petra
# conjugacy.py - Investigate conjugacy growth in F_2
#
# Group G = < S | R >
# x & y are conjugate iff there exists g in G such that gxg^{-1} = y
#
########

########
# Terminology - legal letters are a-zA-Z
# a^{-1} is a-

import re

S = ["a","b"]
R = []

def conjugate(x,y):
    pass

#List n conjugacy class elements of [x]_c
#
# Specifically, for g in the first n elements of S*
# (SL ordering) that produce distinct elements of [x]_c,
# list gxg^{-1}.
#
# Failsafe:
# If <failsafe> attempts to add new members fail
# in a row, then quit early
# Useful when there is less than n members of [x]_c
def cc(x,n,failsafe=3):
    skip = 0
    
    cc_members = set()
    current = ''

    while (len(cc_members) < n):
        conjugate = reduce(current+x+invert(current))
        current = nextSL(current)
        print(conjugate,'conj, =_G',current+x+invert(current))
        if (conjugate not in cc_members):
            cc_members.add(conjugate)
            skip = 0
        else:
            skip += 1
        if (skip >= failsafe):
            print('fs')
            break
    return cc_members
    
#Invert a word
# aabda becomes a-d-b-a-a-
def invert(w):
    inverse = ''
    for letter in w:
        inverse = letter + '-'+inverse
    return inverse

#Next ShortLex word in S*
#Follows convention of a < a^{-1} < b < b^{-1} < ...
#Otherwise, order determined by order of S.
def nextSL(w):
    #Empty string special case
    if (w == ''):
        return S[0]

    #Semigroup generators in convention order
    Sp = []
    for a in S:
        Sp.append(a)
        Sp.append(a+'-')

    #Find something to go forwards in
    A = wordToArray(w)
    for i in range(1,len(A)+1):
        if (A[-i] != Sp[-1]): #A character isn't the last inverse
            A[-i] = Sp[Sp.index(A[-i])+1]
            #All last characters before the change are reset
            for j in range(1,i):
                A[-j] = S[0]
            return arrayToWord(A)
        if (i == len(A)): #String is all last character
            A = [S[0] for i in range(len(A)+1)]
            return arrayToWord(A)

#Turns a word into an array of characters
def wordToArray(w):
    return re.findall(r'[a-zA-Z]-?',w)

#Turns an array back into a word
def arrayToWord(A):
    return ''.join(A)

#Reduce a word - change all instances of a^{-1}a or aa^{-1} to empty
def reduce(w):
    w_red = w
    while ((w_repl := re.sub(r'([a-zA-Z])(\1-|-\1(?!-))','',w_red)) != w_red):
        w_red = w_repl
    return w_red
