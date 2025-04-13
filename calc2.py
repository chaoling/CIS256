from curses.ascii import isdigit
from typing import List

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
        while len(s) > 0:
            c = s.pop(0)
            if isdigit(c):
                #TODO: convert str to int as operand
                operand = operand * 10 + int(c)
            # deal with left bracket
            if c == '(':
                operand = helper(s) #recursion
            if (not isdigit(c) and c != ' ') or len(s) == 0:
                #push the previous sign and number to stack
                #match c: require python 3.10 or newer
                if sign == '+':
                    stk.append(operand)
                    #TODO:
                elif sign == '-':
                    #TODO:
                    stk.append(-operand)
                # now deal with multiplicaton and division
                elif sign == "*":
                    #TODO: take previous number and push back to the stack
                    stk[-1] = stk[-1] * (operand)
                elif sign == "/":
                    #TODO:
                    stk[-1] = int(stk[-1] / (operand))
                else:
                    pass
                sign = c #record the next sign
                operand = 0 #one operand down, reset the num

            if c == ")":
                break
        #pop numbers out of stack and sum

        #TODO: return sum of the numbers on stack
        return sum(stk)

    return helper(list(s))

def main():
    assert calculator2('3*5+222-1')==236
    assert calculator2('3*(5+2)-1')==20

if __name__ == "__main__":
    main()