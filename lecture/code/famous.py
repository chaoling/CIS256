'''
LC 277 Find Celebrity
given the social relationship of n people, find the Celebrity
1. Celebrity is known by everyone else
2. Celebrity don't know anyone else

infer: there is only maximum one person that is celebrity. (why?)

we can use adj matrix (or adj table) to descibe the relationship
'''

def knows(i: int, j: int) -> bool:
    pass

def findCelebrity(n: int) -> int: #O(N^2)
    for candidate in range (n):
        for other in range (n):
            if candidate == other: 
                continue
            if knows(candidate,other) or not knows(other,candidate):
                break #candidate is not a celebrity
        else:
            return candidate
    return -1

def findCelebrity2(n: int) ->int: #O(N) and O(1) space
    cand = 0
    for other in range(1,n):
        if not knows(other, cand) or knows(cand, other):
            cand = other #eliminate current candidate, it can not be celebrity
        else:
            #other is not celebrity
            pass
    
    #now check if candidate is celebrity
    for other in range(0,n):
        if cand == other:
            continue
        if not knows(other,cand) or knows(cand, other):
            return -1

    return cand

