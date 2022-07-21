########
#
# Lynn & Petra
# conjugacyF2.py - Investigate conjugacy growth in F_2
#
# Group G = < S | R >
# x & y are conjugate iff there exists g in G such that gxg^{-1} = y
#
########

########
# Terminology - legal letters are a-zA-Z
# a^{-1} is a-

import re
import conj_lib as cl

S = ["a","b"]
R = []

#Conjugacy growth - number of conjugacy classes whose
#unique geodisic up to conjugacy is n away from the origin
#Aka the growth function of ConjSL (Though the rep. isn't
#necessarily shortlex, it is unique and short)
#
# numCC - number of conjugacy classes to take geodisics of
# if conjSLGrowth(n+1) = 0, then increase this
def conjSLGrowth(n,numCC=100):
    reg = re.compile(r'^([A-Za-z)]-?){'+str(n)+'}$')
    CC = listClasses(numCC)
    return len(list(filter(reg.match,CC)))
    

#List various conjugacy classes and members
# k - desired number of classes
# n - desired number of rep.s per class shown
# p - T/F, print output
def listClasses(k,n=5,p=False):
    if p: print('Conjugacy Classes')
    word = ''
    ccGeos = set()
    numCCs = 0
    
    while numCCs < k:
        word = cl.nextSL(word,S) #Skip empty word
        if cl.reduce(word) == '':
            continue
        
        conjClass = cc(word,failsafe=15)

        #Skip repeats
        if not ccGeos.isdisjoint(conjClass):
            continue
        
        conjClassArray = [ cl.wordToArray(w) for w in conjClass]
        conjGeo = cl.arrayToWord(min(conjClassArray,key=len))
        ccGeos.add(conjGeo)
        ccList = sorted(list(conjClassArray),key=len)[:n]
        ccShort = [cl.arrayToWord(A) for A in ccList]
        if p: print(conjGeo,':',ccShort)
        numCCs += 1
    return ccGeos

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
# failsafe = -1 implies no failsafe
#
# Example of usage:
# 'aba-b-' in cc('ab-')
def cc(x,n=1000,failsafe=-1):
    skip = 0
    
    cc_members = set()
    current = ''

    while (len(cc_members) < n):
        conjugate = cl.reduce(current+x+cl.invert(current))
        #print(conjugate,'=_G',current+x+invert(current),'(',current,')')
        current = cl.nextSL(current,S)
        if (conjugate not in cc_members):
            cc_members.add(conjugate)
            skip = 0
        else:
            skip += 1
        if (skip == failsafe):
            #print('fs')
            break
    return cc_members
