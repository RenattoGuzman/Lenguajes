from BinaryTree import buildTree, ArrayInArray
#from AFN import generateAFN

# Métodos de transfroemación infix a postfix utilizando shunting yard

exp = []
operators = ['*', '|', "'.'", '(', ')']
# extra operators: ?, +

ops = {'*': 3, "'.'": 2, '|': 1}

def flatten(arr):
    result = []
    for item in arr:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result



# Transformar los operdores abreviados a su forma completa
# Ejemplo: a*b?c -> a*(b|ε)c
# Ejemplo: a*b+c -> a*(bb*)+c
# versión mejorada de la función translate
def trans(exp):
    # el recorrido se hace de derecha a izquierda para evitar problemas con los índices
    i = len(exp) - 1
    while i >= 0:
        temp = exp[i]
        if exp[i] == '*':
            if exp[i-1] == '*':
                j = i 
                while exp[j] == '*':
                    j -= 1
                exp = exp[:j+1] + exp[i:]
                i = j+1
                #print(exp)
        elif exp[i] == '?':
            if exp[i-1] == ')':
                j = i
                while exp[j] != '(':
                    j -= 1
                exp2 = exp[j:i]
                exp = exp[:j] + '(' + exp2 + '|ε)' + exp[i+1:]
                i = j+1
            else:
                exp = exp[:i-1] + '(' + exp[i-1] + '|ε)' + exp[i+1:]
        elif exp[i] == '+':
            if exp[i-1] == ')':
                j = i
                while exp[j] != '(':
                    j -= 1
                exp2 = exp[j:i]
                exp3 = exp[:j]
                exp = exp[:j] + '(' + exp2 + exp2 + '*' + ')' + exp[i+1:]
                i = j+1
            else:
                exp = exp[:i-1] + '(' + exp[i-1] + exp[i-1] + '*' + ')' + exp[i+1:]
        i -= 1
    flag = False
    for e in exp:
        if e == '+' or e == '?':
            flag = True
    if flag:
        exp = trans(exp)
    return exp

# trans_3 versión de lista


"""depricated"""
def trans3(lst):
    i = len(lst) - 1
    while i >= 0:
        temp = lst[i]
        if lst[i] == '*':
            if lst[i-1] == '*':
                j = i 
                while lst[j] == '*':
                    j -= 1
                lst = lst[:j+1] + lst[i:]
                i = j+1
                #print(lst)
        elif lst[i] == '?':
            if lst[i-1] == ')':
                j = i
                while lst[j] != '(':
                    j -= 1
                exp2 = lst[j:i]
                lst = lst[:j] + ['(', exp2, '|ε', ')'] + lst[i+1:]
                i = j+1
            else:
                lst = lst[:i-1] + ['(', lst[i-1], '|ε', ')'] + lst[i+1:]
        elif lst[i] == '+':
            if lst[i-1] == ')':
                j = i
                while lst[j] != '(':
                    j -= 1
                exp2 = lst[j:i]
                exp3 = lst[:j]
                lst = lst[:j] + ['(', exp2, exp2, '*', ')'] + lst[i+1:]
                i = j+1
            else:
                lst = lst[:i-1] + ['(', lst[i-1], lst[i-1], '*', ')'] + lst[i+1:]
        i -= 1
    return lst


# ESTA ES LA 
def trans4(exp):
    i = len(exp) - 1
    while i >= 0:
        temp = exp[i]
        #print(' + temp: ', temp)
        if exp[i] == '*':
            if exp[i-1] == '*':
                j = i 
                while exp[j] == '*':
                    j -= 1
                exp = exp[:j+1] + exp[i:]
                i = j+1
        elif exp[i] == '?':
            if exp[i-1] == ')':
                j = i
                while exp[j] != '(':
                    j -= 1
                exp2 = exp[j:i]
                exp = exp[:j] + ['(', exp2, '|', 'ε', ')'] + exp[i+1:]
                i = j+1
            else:
                exp = exp[:i-1] + ['(', exp[i-1], '|', 'ε', ')'] + exp[i+1:]
        elif exp[i] == '+':
            if exp[i-1] == ')':
                j = i
                while exp[j] != '(':
                    j -= 1
                exp2 = exp[j:i]
                exp3 = exp[:j]
                exp = exp[:j] + ['(', exp2, exp2, '*', ')'] + exp[i+1:]
                i = j+1
            else:
                exp = exp[:i-1] + ['(', exp[i-1], exp[i-1], '*', ')'] + exp[i+1:]
        i -= 1
    flag = False
    for e in exp:
        if e == '+' or e == '?':
            flag = True
    if flag:
        exp = trans(exp)

    exp = [str(x) if isinstance(x, str) else trans4(x) for x in exp]
    #return ''.join(exp)

    return [x if isinstance(x, str) else trans4(x) for x in exp]




def trans2(exp):        # el recorrido se hace de derecha a izquierda para evitar problemas con los índices
    i = len(exp) - 1
    while i >= 0:
        temp = exp[i]
        if exp[i] == '*':
            if exp[i-1] == '*':
                j = i 
                while exp[j] == '*':
                    j -= 1
                exp = exp[:j+1] + exp[i:]
                i = j+1
                #print(exp)
        elif exp[i] == '?':
            if i < len(exp)-1:
                t2 = exp[i+1]
                if exp[i+1] == ')':
                    #print('here')
                    j = i
                    while exp[j] != '(':
                        j -= 1
                    exp2 = exp[j:i]
                    exp = exp[:j] + exp2 + '|ε' + exp[i+1:]
                    #added_parens.append((j, i+1))
                    i = j+1
            if exp[i-1] == ')':
                j = i
                while exp[j] != '(':
                    j -= 1
                exp2 = exp[j:i]
                exp = exp[:j] + '(' + exp2 + '|ε)' + exp[i+1:]
                #added_parens.append((j, i+1))
                i = j+1
            else:
                exp = exp[:i-1] + '(' + exp[i-1] + '|ε)' + exp[i+1:]
                #added_parens.append((i-1, i+1))
        elif exp[i] == '+':
            if exp[i-1] == ')':
                j = i
                while exp[j] != '(':
                    j -= 1
                exp2 = exp[j:i]
                exp3 = exp[:j]
                exp = exp[:j] + '(' + exp2 + exp2 + '*' + ')' + exp[i+1:]
                #added_parens.append((j, i+1))
                i = j+1
            else:
                exp = exp[:i-1] + '(' + exp[i-1] + exp[i-1] + '*' + ')' + exp[i+1:]
                #added_parens.append((i-1, i+1))
        i -= 1
    flag = False
    for e in exp:
        if e == '+' or e == '?':
            flag = True
    if flag:
        exp = trans(exp)

    return exp




# Primera función de validación de la expresión regular
# Verifica que los paréntesis estén balanceados, de otra forma
# no se puede realizar la transformación y se debe indicar al usuario
# que la expresión regular no es válida
def parenthesis_check(exp):
    acu = 0
    open_parenthesis = False
    for e in exp:
        if e == '(':
            acu += 1
            open_parenthesis = True
        elif e == ')':
            acu -= 1
            open_parenthesis = False
    if acu == 0 and not open_parenthesis:
        return True
    else:
        return False


def remove_extra_parentheses(exp):
    """
    Removes extra parentheses from a regular expression.

    Parameters:
        exp (str): The regular expression to remove extra parentheses from.

    Returns:
        str: The regular expression with extra parentheses removed.
    """
    # Split the regular expression into characters
    chars = list(exp)

    # Initialize a stack to keep track of parentheses
    stack = []

    # Loop through each character in the expression
    i = 0
    while i < len(chars):
        c = chars[i]

        # If the character is an opening parenthesis, push it onto the stack
        if c == '(':
            stack.append(i)
            i += 1

        # If the character is a closing parenthesis, check if it has a matching opening parenthesis
        elif c == ')':
            if len(stack) > 0:
                # If there is a matching opening parenthesis, remove both parentheses
                stack.pop()
                if i == len(chars) - 1 and stack:
                    i += 1
                else:
                    chars.pop(i)
                    if stack:
                        chars.pop(stack.pop())
            else:
                # If there is no matching opening parenthesis, ignore the closing parenthesis
                i += 1

        # If the character is not a parenthesis, move to the next character
        else:
            i += 1

    # Join the remaining characters back into a string
    result = ''.join(chars)

    return result



# Función que verifica que la expresión regular no tenga errores
# Caso 1: No alimentarle las entradas necesarias a los operadores unarios y binarios
# Caso 2: Alimentarle a un operador binario una entrada que no sea un símbolo o un paréntesis o un operador binario
def symbol_check(exp):
    flag = True
    
    #symbols = ['*', '|', '(', ')']
    for i in range(len(exp)):
        e = exp[i]
        #print(e)
        if e == '*':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(':
                #print('here1')
                flag = False
        elif e == '|':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(' or i == len(exp)-1:
                #print('here2')
                flag = False
            else:
                if exp[i+1] == '|' or exp[i+1] == ')' or exp[i+1] == '*' or exp[i+1] == '.' or exp[i+1] == '+' or exp[i+1] == '?':
                    flag = False
        elif e == '.':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(' or i == len(exp)-1:
                #print('here3')
                flag = False
            else:
                if exp[i+1] == '|' or exp[i+1] == ')' or exp[i+1] == '*' or exp[i+1] == '.' or exp[i+1] == '+' or exp[i+1] == '?':
                    #print('here4')
                    flag = False
        elif e == '(':
            if i == len(exp)-1:
                #print('here5')
                flag = False
            else:
                if exp[i+1] == '|' or exp[i+1] == ')' or exp[i+1] == '*' or exp[i+1] == '.' or exp[i+1] == '+' or exp[i+1] == '?':
                    #print('here6')
                    flag = False
        elif e == '+':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(':
                #print('here7')
                flag = False
        elif e == '?':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(':
                #print('here8')
                flag = False

        
    return flag
                
    
#  Esta versión del método supone la inexistencia de operadores de concatenación en la expresión regular
def symbol_check_2(exp):
    flag = True
    
    #symbols = ['*', '|', '(', ')']
    for i in range(len(exp)):
        e = exp[i]
        #print(e)
        if e == '*':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(':
                #print('here1')
                flag = False
        elif e == '|':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(' or i == len(exp)-1:
                #print('here2')
                flag = False
            else:
                if exp[i+1] == '|' or exp[i+1] == ')' or exp[i+1] == '*' or exp[i+1] == '+' or exp[i+1] == '?':
                    flag = False
        elif e == '(':
            if i == len(exp)-1:
                #print('here5')
                flag = False
            else:
                if exp[i+1] == '|' or exp[i+1] == ')' or exp[i+1] == '*' or exp[i+1] == '+' or exp[i+1] == '?':
                    #print('here6')
                    flag = False
        elif e == '+':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(':
                #print('here7')
                flag = False
        elif e == '?':
            if i == 0 or exp[i-1] == '|' or exp[i-1] == '(':
                #print('here8')
                flag = False

        
    return flag


#Función necesaria para leer la expresión regular y agregar los operadores de concatenación
def readExp(exp):
    infix = []
    abc = [] 
    symbols = ['*', '|', '(', ')']
    #exp = input('Ingrese la expresion regular: \n')
    exp2 = ''
    for e in exp:
        infix.append(e)
        if e not in symbols and e not in abc:
            abc.append(e)
    size = len(infix)
    kleene = False
    waiting  = 0
    while size > 0:
        if size > 1:
            v1 = infix[size-1]
            v2 = infix[size-2]
            if kleene:
                if waiting > 0:
                    waiting -= 1
                    kleene = False                    
                    waiting = 0
            elif v1 == '*' and not kleene:
                kleene = True
                waiting = 1
            if (v1 == '(' and v2 in abc and not kleene) or (v1 in abc and v2 == ')' and not kleene) or (v1 in abc and v2 in abc and not kleene) or (v1 == '(' and v2 == ')' and not kleene) or (v1 in abc and v2 == '*' and not kleene) or (v1 == '(' and v2 == '*' and not kleene):
                exp2 = '.' + v1 + exp2
            else:
                exp2 = v1 + exp2
            size -= 1
        else:
            v1 = infix[size-1]
            exp2 = v1 + exp2
            size -= 1
    #exp2 = exp2 + '.#'
    return exp2

# same as readExp, but for the list format
def readExp_2(exp):
    infix = []
    abc = [] 
    symbols = ['*', '|', '(', ')']
    exp2 = []
    for e in exp:
        infix.append(e)
        if e not in symbols and e not in abc:
            abc.append(e)
    size = len(infix)
    kleene = False
    waiting = 0
    #print('Xanathar, the beholder\n')
    while size > 0:
        if size > 1:
            v1 = infix[size - 1]
            v2 = infix[size - 2]
            if kleene:
                if waiting > 0:
                    waiting -= 1
                    kleene = False
                    waiting = 0
            elif v1 == '*' and not kleene:
                kleene = True
                waiting = 1
            if (
                (v1 == '(' and v2 in abc and not kleene) or
                (v1 in abc and v2 == ')' and not kleene) or
                (v1 in abc and v2 in abc and not kleene) or
                (v1 == '(' and v2 == ')' and not kleene)
            ):
                exp3 = exp2.copy()
                exp2.insert(0, v1)
                exp2.insert(0, "'.'")
            else:
                if v1 in abc and v2 == '*' and not kleene:
                    exp2.insert(0, "'.'")
                exp2.insert(0, v1)
            size -= 1
        else:
            v1 = infix[size - 1]
            exp2.insert(0, v1)
            size -= 1
    #print('\nArkhan the cruel')
    #print('\n', ' '.join(str(e) for e in exp2))
    return exp2





#Basado en el algortimo de Shunting-yard
def InfixToPostfix(exp):
    if parenthesis_check(exp) and symbol_check_2(exp):
        #print('La expresion regular es válida: ', ' '.join(exp))
        print('La expresion regular es válida')
        #exp = trans(exp)

        #exp = readExp(exp)
        if isinstance(exp, list):
            #print(exp)
            exp = trans4(exp)
            #print('Vecna the whispered one')
            #print(type(exp))
            exp = flatten(exp)
            #print('Gruumsh the destroyer')
            #print(' '.join(str(e) for e in exp))
            #print('Tiamat the ancient one')
            exp = readExp_2(exp)
            #exp = readExp_3(exp)
            #print(exp)
            #print(' '.join(str(e) for e in exp))
            #print('Bahamut the golden')

        else:
            exp = trans(exp)
            exp = readExp(exp)
        #print(isinstance(exp, list))
        print('La expresion regular transformada es: ', ''.join(str(e) for e in exp))
        #print(exp)
        OpStack = []
        postfix = []
        for e in exp:
            #If the input symbol is a letter… append it directly to the output queue
            #print('postfix: ', postfix)
            #print('OpStack: ', OpStack)
            #print('e: ', e)
            #print('-------------------')
            if e not in operators:
                postfix.append(e)
            else:
                if e == '(':
                    OpStack.append(e)
                #elif e == ')' and OpStack[-1] != '(' and len(OpStack) > 0:
                elif e == ')' and len(OpStack) > 0:
                    while OpStack[-1] != '(':
                        postfix.append(OpStack.pop())
                    OpStack.pop()
                else:
                    if len(OpStack) > 0:
                        while len(OpStack) > 0 and OpStack[-1] != '(' and ops[e] <= ops[OpStack[-1]]:
                            postfix.append(OpStack.pop())
                    OpStack.append(e)
        while len(OpStack) > 0:
            postfix.append(OpStack.pop())
        #postfix.append('#')
        #postfix.append('.')
        #exp_postfix = ''.join(postfix)
        #return exp_postfix
        return postfix
    else:
        # return 'La expresión regular no es válida, verifique que los paréntesis estén balanceados'
        print('La expresión regular no es válida. Symbol check: ', symbol_check_2(exp), ' Parenthesis check: ', parenthesis_check(exp))
        return False


# expresiones regulares de prueba válidas en forma expandida, no concatenadas
#exp = 'abc'
# exp = 'a|b'
# exp = 'a|b|c'
# exp = '(a|b)*'s
# exp = '(a|b)*c'
# exp = '(a|b*)**cd'
#exp  = 'a**b*c|d'

#exp = '(a|b)*abb(a|b)*'

# expresiones regulares de prueba válidas en forma abreviada
#exp = 'a*b?**c+'
#exp = 'a*b+c'
#exp = 'a*b+c*'
#exp = 'a*b+c*|d'
#                     exp = 'a**(b|c)?*(da+)?a(c|d*)+'
#exp = '(a?|b+)***c**'
#exp = '(a|b+)+'
#exp = '(a***|b****)***'
#exp = '(a|b)*abb'


# expresiones regulares de prueba inválidas
#exp = ')a|b('

#print('Expresión regular: ', exp)
#print('Expresión regular en forma abreviada: ', translate(exp))
#print('Expresión simplificada: ', trans(exp))
#sprint(parenthesis_check(exp))


#exp = '0?(1?)?0*'
## exp = '(0|ε)((1|ε)|ε)0*'
#
##exp = InfixToPostfix(exp)
##
##
#print('Expresión regular postfix: ', trans(exp))
#print('Expresión regular postfix: ', trans2(exp))
#print('Expresión regular postfix: ', remove_extra_parentheses(trans2(exp)) )
#for e in exp: 
#   print(e)
#exp = list(exp)
#syntactic_tree = buildTree(exp.pop(), exp)  



## print('\n\n')
## print('Árbol sintáctico: ', syntactic_tree)
## print(syntactic_tree.traversePostOrder())#
## print('\n\n')
## syntactic_tree.post2()
## syntactic_tree.determineFollowPos()


#syntactic_tree.post3()
#syntactic_tree.post2()
#syntactic_tree.determineFollowPos()
#syntactic_tree.post3()
#
##print('Expresión regular 2: ', InfixToPostfix(exp))
#
 


#   foul = [
#       'a+b*c',
#       '(a(b|c)*',
#       'ab(cd)+',
#       '[a-z])*',
#       'ab|c*def',
#       '.+.+*',
#       '\d?[a-z]+',
#       '(?i)dog|cat|mouse',
#       'a?b+c*'
#       ]#   

#   for e in foul:
#       print('Expresión regular: ', e)
#       if parenthesis_check(e):
#           #print('La expresión regular es válida')
#           print(symbol_check(e))
#       else:
#           print('La expresión regular no es válida')#   