def infix_to_prefix(infix):
    #infix = infix.replace(" ", "")
    infix = infix.replace("**", "^")
    # Function to convert infix to prefix expression
    def precedence(op):
        # Returns the precedence of the operator
        if op in ['+', '-']:
            return 1
        if op in ['*', '/']:
            return 2
        if op in ['^']:
            return 3
        return 0

    def is_operator(op):
        # Returns true if the operator is an operator
        return op in ['+', '-', '*', '/', '^']

    lastToken = ''
    lastIsNum = False
    tokenUsed = False
    stack = []
    output = []
    for token in reversed(infix):
        tokenUsed = False
        if lastIsNum is True:
            if token == '-':
                output.append('-%s' % lastToken)
                lastIsNum = False
                tokenUsed = True
            elif token == '+' or token == ' ':
                output.append(lastToken)
                lastIsNum = False
                tokenUsed = True
            else:
                tokenUsed = False
            
        if tokenUsed is False:
            if token == ' ':
                continue
            if is_operator(token):
                while stack and precedence(token) < precedence(stack[-1]):
                    output.append(stack.pop())
                stack.append(token)
            elif token == ')':
                stack.append(token)
            elif token == '(':
                while stack[-1] != ')':
                    output.append(stack.pop())
                stack.pop()
            else:
                lastToken = token
                lastIsNum = True
        
    while stack:
        output.append(stack.pop())

    output.reverse()
    return output

if __name__ == '__main__':
    s = "((x + y) ** -z) / w + +u"
    print(infix_to_prefix(s))
