from curses.ascii import isdigit
from typing import List


def calculator(s: str) -> int:
    '''
    1-12+3 => +1 , -12, +3 , push them to stack, then pop and add
    multiply and division:
    2-3*4+5 => +2, -3, *4, +5
    we ignore white space as well
    '''

    stk = [] #here we use python list as a stack.
    operand = 0 #convert str to number as one operand
    sign = '+' #assume first number is always positive
    total = 0  #final answer
    
    for i,c in enumerate(s):
        if isdigit(c):
            #TODO: convert that digit to int and append to the int num
            temp = str(operand) + c
            operand = int(temp)

        if (not isdigit(c) and c != ' ') or i == len(s) -1:
            #push the previous sign and number to stack
            #match c: require python 3.10 or newer
            if sign == '+':
                #TODO:
                stk.append(operand)
            elif sign == '-':
                #TODO:
                stk.append(-abs(operand))
            # now deal with multiplicaton and division
            elif sign == "*":
                #TODO: take previous number and push back to the stack
                temp = stk[-1] * operand
                stk[-1] = temp
            elif sign == "/":
                #TODO:
                temp = stk[-1] / operand
                stk[-1] = temp
            else:
                pass
            sign = c #record the next sign
            operand = 0 #one operand down, reset the num

    #pop numbers out of stack and sum
    #TODO:
    for n in range(len(stk)):
        number = stk.pop()
        total += number
    return total


def calculator2(s: str) -> int:
    '''
    how to deal with brackets: use recursion
    calculate(`3*(4-5/2)-6`)
    = 3 * calculate(`4-5/2`) - 6
    = 3 * 2 - 6
    = 0
    1-12+3 => +1 , -12, +3 , push them to stack, then pop and add
    multiply and division:
    2-3*4+5 => +2, -3, *4, +5
    we ignore white space as well
    '''
    def helper(s: List) -> int:
        #stk = deque()
        stk = []
        operand = 0
        sign = '+'  # assume first number is always positive
        total = 0
        
        while len(s) > 0:
            c = s.pop(0)
            if isdigit(c):
                #TODO: convert str to int as operand
                temp = str(operand) + c
                operand = int(temp)
            # deal with left bracket
            if c == '(':
                operand = helper(s) #recursion
            if (not isdigit(c) and c != ' ') or len(s) == 0:
                #push the previous sign and number to stack
                #match c: require python 3.10 or newer
                if sign == '+':
                    #TODO:
                    stk.append(operand)
                elif sign == '-':
                    #TODO:
                    stk.append(-abs(operand))
                # now deal with multiplicaton and division
                elif sign == "*":
                    #TODO: take previous number and push back to the stack
                    temp = stk[-1] * operand
                    stk[-1] = temp
                elif sign == "/":
                    #TODO:
                    temp = stk[-1] / operand
                    stk[-1] = temp
                else:
                    pass
                sign = c #record the next sign
                operand = 0 #one operand down, reset the num

            if c == ")":
                break
        #pop numbers out of stack and sum
        #TODO: return sum of the numbers on stack
        for n in range(len(stk)):
            number = stk.pop()
            total += number
        return total
    return helper(list(s))


def main():
    c1 = calculator('3*5+222-1')
    c2 = calculator2('3*5+222-1')
    assert c1 == c2, f"{c1=}{c2=}"
    assert c1 == 236
    test2 = calculator2('3*(5+2)-1')
    assert test2 == 20, test2 

if __name__ == "__main__":
    main()