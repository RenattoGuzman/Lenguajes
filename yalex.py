
operators = ["+", "*", "?", "|", "(", ")", ".", "[", "]"]

# validar la existencia de reglas repetidas
def repeated_rule(r, l):
    # Check for invalid rule names
    for key in r:
        if len(key) > 1 and key not in l:
            # Ignore rule names with quotes
            if key.count("'") == 2 or key.count('"') == 2:
                continue
            raise Exception("Invalid rule name: " + key)


# generar la gramatica a partir del archivo .yal
def grammar(file):
    with open(file, 'r') as f:
        yal = f.read().splitlines()
        let_rules = []

        for l in yal:
            nl = l.strip()

            if nl != '' and nl[0] != '#':
                #print(nl)
                if '(*' in nl:
                    #print(nl.index('(*'))
                    nl = nl[:nl.index('(*')]
                    nl = nl.strip()
                    #print(' - ', nl)
                    if nl != '':
                        let_rules.append(nl)
                else:
                    let_rules.append(nl)
        lets = []
        rules = []
        rulesFlag = False

        for e in let_rules: 
            if rulesFlag:
                rules.append(e)
            else:
                if e.startswith('rule'):
                    rulesFlag = True
                    #print('rules')
                else:
                    lets.append(e)

        l = {} # let
        r = {} # rules

        # diccionario de reglas de formato let
        for let in lets:

            # separar la sentencia let en dos partes, la variable y el valor
            let = let.replace("let ", "")
            let = let.strip()
            let = let.split("=")

            letVal = let[1].strip()

            # valor de la sentencia let en forma de arreglo
            if letVal.startswith("[") and letVal.endswith("]"):
                # si el valor arreglo tiene un rango
                if "-" in letVal:
                    letVal = letVal[1:-1]
                    #print(' - ', let ,' let interval value: ',letVal)

                    tempArray = []
                    lastIndex = 0
                    count = letVal.count("-")

                    for x in range(count):
                        index = letVal.index("-", lastIndex)

                        startA = letVal.index("'", lastIndex)
                        endA = letVal.index("'", startA + 1)

                        startB = letVal.index("'", index)
                        endB = letVal.index("'", startB + 1)

                        valA = letVal[startA + 1:endA]
                        valB = letVal[startB + 1:endB]

                        tempArray.append(valA + "-" + valB)

                        lastIndex = endB + 1

                # si el valor arreglo no tiene un rango, sino que
                # es un arreglo de caracteres especificos
                else:

                    #print(' - ', let ,' let array value: ',letVal)

                    testCount = letVal.count("'")
                    if testCount == 0:
                        testCount = letVal.count('"')

                    if testCount > 2:
                        letVal = letVal[1:-1]

                        tempArray = []
                        currentIndex = -1
                        for x in range(len(letVal)):
                            char = letVal[x]

                            if currentIndex > x:
                                continue
                            elif currentIndex == x:
                                currentIndex = -1

                            if char == "'":
                                if currentIndex == -1:
                                    currentIndex = x

                            elif currentIndex != -1:
                                start = currentIndex + 1
                                end = letVal.index("'", start)

                                tempArray.append(letVal[start:end])
                                currentIndex = end + 1

                    else:
                        letVal = letVal[1:-1]

                        if "\\" in letVal:
                            letVal = letVal[1:-1]

                            tempArray = []
                            for char in letVal:
                                if char != "\\":
                                    tempArray.append("\\" + char)

                        else:
                            tempArray = []
                            for char in letVal:
                                if char != "'" and char != '"':
                                    tempArray.append(char)

                letVal = tempArray

            l[let[0].strip()] = letVal

        # diccionario de reglas de formato rule
        for rule in rules:
            #print(' - ', rule ,' rule value: ')
            rule = rule.replace("rule ", "")
            if "return" in rule:
                start = rule.index("{")
                end = rule.index("}")
                returnVal = rule[start + 1:end].strip() + rule[end + 1:].strip()

                if "'" in rule:
                    start = rule.index("'")
                    end = rule.index("'", start + 1)
                    ruleName = rule[start + 1:end].strip()
                else:
                    start = 0
                    if "|" in rule:
                        start = rule.index("|") + 1

                    end = rule.index("{")
                    ruleName = rule[start:end].strip()
                r[ruleName] = returnVal
            else:
                r[rule.strip()] = ""

        repeated_rule(r, l)

        return l, r


# generar el alfabeto a partir de las reglas let y rule
# además de generar el regex a partir de las reglas rule
def generate_alphabet(l, r):
    alphabet = []
    operators = ["[", "]", "|", "'", "\""]
    regex = []

    for key in l:
        if isinstance(l[key], list):
            newVals = []
            case = 0

            for val in l[key]:
                if isinstance(val, str) and "-" in val:
                    case = 1
                    break
                elif isinstance(val, str) and "\\" in val:
                    case = 2
                    break

            if case == 1:
                for val in l[key]:
                    start = ord(val[0])
                    end = ord(val[2])

                    for x in range(start, end + 1):
                        alphabet.append(chr(x))
                        newVals.append(chr(x))

                l[key] = newVals

            elif case == 2:
                newVals = []
                for val in l[key]:
                    if val.startswith("\\"):
                        val = val.replace("\\", "")

                        if val == "n":
                            newVals.append(ord("\n"))
                        elif val == "t":
                            newVals.append(ord("\t"))
                        elif val == "r":
                            newVals.append(ord("\r"))
                        elif val == "f":
                            newVals.append(ord("\f"))
                        elif val == "s":
                            newVals.append(ord(" "))
                        else:
                            raise Exception("Invalid escape character: " + val)
                    else:
                        newVals.append(ord(val))

                for val in newVals:
                    alphabet.append(val)

                l[key] = newVals

            else:
                for val in l[key]:
                    alphabet.append(val)

    for key in r:
        if key in l:
            val = l[key]
            x = 0

            while True:
                if val[x] in operators:
                    if val[x] == "[":
                        x += 1
                        regex.append("(")

                        while not val[x] == "]":
                            if val[x] != "'":
                                if val[x] in operators or val[x] == "-":
                                    regex.append("'" + str(ord(val[x])) + "'")
                                    alphabet.append(ord(val[x]))
                                else:
                                    regex.append(val[x])
                                    alphabet.append(val[x])

                                regex.append("|")

                            x += 1

                        regex.pop()
                        regex.append(")")

                        x += 1

                    else:
                        x += 1

                else:
                    tempStr = ""
                    while not val[x] in operators:
                        tempStr += val[x]
                        x += 1

                        if x >= len(val):
                            break

                    if tempStr in l and isinstance(l[tempStr], str):
                        tempOperators = ""
                        newTempStr = ""

                        for char in l[tempStr]:
                            if char in operators:
                                tempOperators += char
                            else:
                                newTempStr += char

                        if newTempStr in l:
                            regex.append(newTempStr)

                            for char in tempOperators:
                                regex.append(char)
                                regex.append("|")

                            regex.pop()

                        else:
                            regex.append(tempStr)

                    else:
                        if "'" in tempStr:
                            tempStr = tempStr.replace("'", "")

                        if len(tempStr) > 0:
                            if len(tempStr) == 1:
                                alphabet.append(tempStr)

                            regex.append(tempStr)

                    if x >= len(val):
                        break

            if key != list(r.keys())[-1]:
                regex.append("|")

        else:
            for char in key:
                regex.append("'" + str(ord(char)) + "'")
                alphabet.append(ord(char))
                regex.append("|")

            regex.pop() # Remove last "|"
            if key != list(r.keys())[-1]:
                regex.append("|")


    return alphabet, regex


import re 

def separator(exp):
    pattern = "|".join(re.escape(operator) for operator in operators)
    separated_string = re.split(f"({pattern})", exp)
    separated_string = [s for s in separated_string if s]  # Remove empty elements
    return separated_string

def replace_with_separated_elements(array):
    updated_array = []
    for element in array:
        if any(operator in element for operator in operators):
            separated_elements = separator(element)
            updated_array.extend(separated_elements)
        else:
            updated_array.append(element)
    return updated_array

def merge_elements(array, start_index, end_index, merged_element):
    merged_array = array[:start_index] + [merged_element] + array[end_index + 1:]
    return merged_array


def uniteTokens(array):
    flag = False
    temps = []
    temp = ""
    pos_is = []
    pos_fs = []
    for i in range(len(array)):
        #print('  *  ',array[i])
        if array[i] == "'" and not flag:
        #    print('here1')
            flag = True
            pos_is.append(i)
            temp += array[i]
        elif array[i] == "'" and flag:
       #     print('here2')
            flag = False
            pos_fs.append(i)
            temp += array[i]
            temps.append(temp)
      #      print('temp: ', temp)
            temp = ""
        elif flag:
     #       print('here3')
            temp += array[i]
    #print('temp: ', temp)
    #print('temps: ', temps)
    #print('pos_is: ', pos_is)
    #print('pos_fs: ', pos_fs)
    for i in range(len(pos_is)):
        #print('  *  ', pos_is[i], pos_fs[i], temps[i])
        array = merge_elements(array, pos_is[i], pos_fs[i], temps[i])
        #for e in array:
            #print('  *//  ', e)
    return array
    
            



def orArray(array):
    temp = ""
    temp += "("
    for e in array:
        temp += str(e)
        if e != array[-1]:
            temp += "|"
    temp += ")"
    return temp

def ElementofArrayinArray(array, array2):
    #print(' GUUUUUUTS', array2)
    for e in array:
        #print(' + e: ', e)
        if e in array2:
            #print(' GRIFFIIIITH')
            return True
    return False



# Traducir un elemento defindo en lets a su valor en sigma
# Existen algunos casos en donde su valor es otro elemento de lets
# por lo que se debe de traducir recursivamente
def translate(l, lets):
    r = lets[l]
    for e in lets:
        if e in r:
            #print('Vamos aqui: ', e, r)
            temp_r = separator(r)
            #print('temp_r: ', temp_r)
            for i in range(len(temp_r)):
                if temp_r[i] in lets:
                    temp_r[i] = translate(temp_r[i], lets)
            #print('temp_r: ', temp_r)
            r = temp_r
    if not isinstance(r, str) and not ElementofArrayinArray(r, operators):
        r = orArray(r)
    #print(' - r: ', r)
    return r



# traducir el regex a partir de las reglas ya definidas
def parser(regexStack, lets, sigma):
    print('Stack String: ', ''.join(regexStack))
    regex = ""
    regex2 = []
    print('-'*100)

    
    for val in regexStack:
        #print("val: ", val)
        if val not in lets:
            val = val.strip("'")
            regex += val
            regex2.append(val)
        else:
            #print("val: ", val)
            #print("lets[val]: ", lets[val])
            regex += lets[val]
            regex2.append(lets[val])
    
    
    print("regex: ", regex2)
    
    print('-'*100)

    # diferenciación entre tokens y operadores
    for i in range(len(regex2)):
        if regex2[i] in sigma and regex2[i] in operators:
            regex2[i] = "'" + str(regex2[i]) + "'"
        
    

    regex2 = replace_with_separated_elements(regex2)
    regex2 = uniteTokens(regex2)

    # Update sigma
    for e in regex2:
        if e not in sigma and e not in operators and e not in lets:
            if type(e) == str and e.isdigit():
                int_e = int(e)
                if int_e not in sigma:
                    sigma.append(int_e)
            else:    
                sigma.append(e)

    print("regexStack: ", regex2)

    for e in regex2:
        if e in lets:
            #print("e: ", e, ' - ', lets[e], ' - ', translate(e, lets))
            replacement = ''.join(translate(e, lets))
            #print("replacement: ", e, ' - ', replacement)
            
            #print("regex: ", regex)
            index = regex2.index(e)
            regex2[index] = replacement
            regex2 = replace_with_separated_elements(regex2)
            #print("regex: ", ''.join(regex2))

    regex2 = uniteTokens(regex2)


        #print("val: ", val)
    print('-'*100)

    print("Regex: ", regex)
    
    return regex2, sigma
