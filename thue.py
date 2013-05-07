#!/usr/bin/python

# thue.py - Aaron Laursen
#
# written for python version 3.3.1
#
# run as:
# python thue.py  rules.txt
#
# also accepts rules on stdin

import fileinput
import random

def main():
    start, rules = readRules()
    print(start)
    print(rules)
    print(runReps(start, rules))
    return

def readRules():
    # reads in a rules file of the form:
    #
    # lhs1::=rhs1 
    # lhs2::=rhs2
    #
    # ::=start_state
    #
    # note that whitespace within lines is relevant,
    # empty lines are ignored,
    # literal "\n" in file if replaced with newline
    rules={}
    start=""
    for line in fileinput.input():
        if "::=" not in line:
            continue
        line=line[:-1].replace("\\n","\n")
        p=line.split("::=")
        if p[0]=="":
            start=p[1]
            continue
        if p[0] not in rules:
            rules[p[0]]=[]
        rules[p[0]].append(p[1])
    return start, rules

def parseRep(s):
    # takes care of ":::" and "~" in rpelacement
    while ":::" in s:
        s.replace(":::",input())
    if "~" in s:
        p=s.split("~",1)
        s=p[0]
        print(p[1])
    return s

def findAll(l,s):
    #finds all occurances of l in s
    if l=="" and s!="":
        return[]
    if l=="" and s=="":
        return [0,]
    p=[]
    i=s.find(l)
    while i !=-1:
        p.append(i)
        i=s.find(l,i+1)
    return p

def runReps(s, rules):
    # repeatedly applies rules to state until it cannot apply more
    while True:
        print("State:"+s)
        cand=[] #generate all posible rule applications
        for l in rules:
            if l not in s: 
                continue
            for p in findAll(l,s):
                for r in rules[l]:
                    cand.append( (l,r,p) )
        if len(cand)==0:
            return s
        i=random.randint(0,len(cand)-1) #pick a rule randomly
        s=applyRule( s,cand[i] )

def applyRule(s, can):
    # takes a state and a candidate tuple and returns new state
    rhs = parseRep(can[1])
    s= s[:can[2]] + rhs + s[can[2]+len(can[0]):]
    return s

main()
