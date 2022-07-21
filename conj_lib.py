########
#
# Lynn & Petra
# conj_lib.py - Library of functions to help work with words and conj. classes
#
# Group G = < S | R >
# x & y are conjugate iff there exists g in G such that gxg^{-1} = y
#
########

########
# Terminology - legal letters are a-zA-Z
# a^{-1} is a-

import re

#Invert a word
# aabda becomes a-d-b-a-a-
def invert(w):
    if not verify(w):
        raise ValueError("Not a valid word")
    A = wordToArray(w)
    A.reverse()
    inverse = [invertLetter(l) for l in A]
    return arrayToWord(inverse)

#Invert a letter
def invertLetter(l):
    if not re.match(r'[a-zA-Z]-?',l):
        raise ValueError("Not a valid letter")
    if re.match(r'.-',l):
        return l[0]
    else:
        return l+'-'

#Next ShortLex word in S*
#Follows convention of a < a^{-1} < b < b^{-1} < ...
#Otherwise, order determined by order of S.
def nextSL(w,S):
    if not verify(w):
        raise ValueError("Not a valid word")
    if not type(S) == list:
        raise TypeError("Not a list of generators")
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
    if not verify(w):
        raise ValueError("Not a valid word")
    return re.findall(r'[a-zA-Z]-?',w)

#Turns an array back into a word
def arrayToWord(A):
    for l in A:
        if not re.match(r'[a-zA-Z]-?',l):
            raise ValueError("Not a valid word")
    return ''.join(A)

#Reduce a word - change all instances of a^{-1}a or aa^{-1} to empty
def reduce(w):
    if not verify(w):
        raise ValueError("Not a valid word")
    w_red = w
    while ((w_repl := re.sub(r'([a-zA-Z])(\1-|-\1(?!-))','',w_red)) != w_red):
        w_red = w_repl
    return w_red

#Verify that this is a valid word
def verify(w):
    return re.match(r'^([a-zA-Z]-?)*$',w)
