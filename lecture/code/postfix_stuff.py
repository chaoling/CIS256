from pythonds.basic.stack import Stack

def infixToPostfix(infixexpr):
    prec = {}
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

def infixToPrefix(infix):
    '''
    convert it by reverse infix expression, replace ( with ) and vice versa,
    so we can reuse infix2postfix function, then reverse the postfix expression
    '''
    infix = infix[::-1]
    #print(f'{infix=}')
    s = infix.split()
    for i,l in enumerate(s):
        if l == '(':
            s[i] = ')'
        elif l == ')':
            s[i] = '('
    s2 = ' '.join(s)
    #print(f'{s2=}')
    ans = infixToPostfix(s2)
    return ans[::-1]


#print(infixToPostfix("A * B + C * D"))
print(infixToPrefix("( A + B ) * ( C + D ) * ( E + F )"))
#print(infixToPrefix("( A + B ) * C - ( D - E ) * ( F + G )"))
#print(infixToPostfix("( A + B ) * C - ( D - E ) * ( F + G )"))

