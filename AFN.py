# Recibimos un arbol sintactico y lo recorremos para generar los diferentes autómatas finitos no deterministas
#from InfixToPostfix import InfixToPostfix
import graphviz as gv

operadores = ['*', '|', "'.'"]

#exp = 'a**(b|c)?*(da+)?a(c|d*)+'
## exp = '(a|b)*a(a|b)(a|b)'
## 
## exp_postfix = InfixToPostfix(exp)

AutomataFND = None

class Node:
    def __init__(self, name):
        self.name = name
        self.isAccept = False
        self.transitions = []

    def checkTransition(self, symbol):
        for t in self.transitions:
            if t.symbol == symbol:
                return t.to
        return None


class Transition:
    def __init__(self, symbol, to):
        self.symbol = symbol
        self.to = to


class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end




def generateAFN(regex):
    # stack de NFAs para construir el AFN final
    NFA_final = []
    i = 0
    for e in regex:
        #print(e)
        if(e in operadores): 
            # Construimos el automata de un operador
            #pass
            #print(e, " operador ")
            if(e == '*'):
                # Construimos el automata de un operador de cerradura
                #pass
                #print(e, " cerradura ")
                # autómata a kleenear
                kleene = NFA_final.pop()
                # estados de inicio y fin del barco
                s1 = Node(i)
                i += 1
                s2 = Node(i)
                # transiciones del barco
                s1.transitions.append(Transition('ε', kleene.start))
                s1.transitions.append(Transition('ε', s2))
                kleene.end.transitions.append(Transition('ε', kleene.start))
                kleene.end.transitions.append(Transition('ε', s2))
                # agregamos el nuevo automata a la pila
                NFA_final.append(NFA(s1, s2))

            elif(e == '|'):
                # Construimos el automata de un operador de union
                #pass
                #print(e, " union ")
                or_1 = NFA_final.pop()
                or_2 = NFA_final.pop()
                # estados de inicio y fin de la hamburguesa
                s1 = Node(i)
                i += 1
                s2 = Node(i)
                # transiciones de la hamburguesa
                s1.transitions.append(Transition('ε', or_1.start))
                s1.transitions.append(Transition('ε', or_2.start))
                or_1.end.transitions.append(Transition('ε', s2))
                or_2.end.transitions.append(Transition('ε', s2))
                # agregamos el nuevo automata a la pila
                NFA_final.append(NFA(s1, s2))

            elif(e == "'.'"):
                # Construimos el automata de un operador de concatenacion
                #pass
                #print(e, " concatenacion ")
                concat_1 = NFA_final.pop()
                concat_2 = NFA_final.pop()
                # transiciones de la concatenacion
                concat_2.end.transitions.append(Transition('ε', concat_1.start))
                # agregamos el nuevo automata a la pila
                NFA_final.append(NFA(concat_2.start, concat_1.end))
                
        else:
            # Construimos el automata simple de una letra
            #pass
            s1 = Node(i)
            i += 1
            s2 = Node(i)
            s1.transitions.append(Transition(e, s2))
            NFA_final.append(NFA(s1, s2))
        i += 1
    #print(len(NFA_final))
    #print("AFN posición inicial: ", NFA_final[0].start.name, " - Posición final", NFA_final[0].end.name)
    #return NFA_final.pop()
    AutomataFND = NFA_final.pop()
    return AutomataFND
                



def visual_AFN(NFA, exp):
    g = gv.Digraph(format='png')
    g.attr('node', shape='circle')
    g.attr('node', style='filled')
    g.attr('node', color='lightblue2')
    g.attr('node', fontcolor='black')
    g.attr('edge', color='black')
    g.attr('edge', fontcolor='black')
    g.attr('edge', fontsize='20')
    g.attr('graph', rankdir='LR')
    g.attr('graph', size='17')

    # add a title to the graph
    g.attr(label=exp)
    
    # agregamos los nodos
    estados = []
    stack = []
    stack.append(NFA.start)

    while(len(stack) > 0):
        nodo = stack.pop()
        if(nodo not in estados):
            estados.append(nodo)
            for t in nodo.transitions:
                g.edge(str(nodo.name), str(t.to.name), label=t.symbol)
                stack.append(t.to)
    
    return g.render('AFN', view=True, directory='./visual_results/')


def simulation(NFA, cadena):
    pass