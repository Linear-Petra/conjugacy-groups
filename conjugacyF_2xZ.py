########
#
# Lynn & Petra
# conjugacyF_2xZ - Messing around with conjugacy classes in F_2 x Z
#
# Group F_2 x Z = < a, b, c | ac = ca, bc = cb >
# x & y are conjugate iff there exists g in G such that gxg^{-1} = y
#
########

import re
import conj_lib as cl

S = ['a','b','c']

# Determine if a word is ShortLex
def isSL(w):
    if not cl.verify(w):
        raise ValueError(w,"is not a valid word")

    return re.match(r'^(?!.*?([a-zA-Z])(\1-|-\1(?!-)))((a-?)*(b-?)*)*(c-?)*$',w) != None
    #Something of the form (a^{i_k} b^{j_k})^k c^l) for k,l,i_k,j_k in Z
    #Equivalent to
    #return (cl.reduce(w) == w) and (re.match(r'^((a-?)*(b-?)*)*(c-)*$',w) != None)

#Reduces a word and makes it so isSL(w) == True
def shortlexify(w):
    if not cl.verify(w):
        raise ValueError(w,"is not a valid word")
    cm_count = w.count('c-')
    c_count = w.count('c') - cm_count
    w_sl = re.sub('c-?','',w) + 'c'*c_count + 'c-'*cm_count #c commutes with all
    w_sl = cl.reduce(w_sl)
    return w_sl

#Search for a bunch of conjugacy class representatives
#See conjugacyF2.py
def cc(w,n=10,failsafe=-1):
    skip = 0
    
    cc_members = set()
    current = ''

    while (len(cc_members) < n):
        conjugate = shortlexify(current+w+cl.invert(current))
        current = cl.nextSL(current,S)
        if (conjugate not in cc_members):
            cc_members.add(conjugate)
            skip = 0
        else:
            skip += 1
        if (skip == failsafe):
            break
    return cc_members

