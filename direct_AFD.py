from BinaryTree import ArrayInArray
from AFN_to_AFD import state
import graphviz


def compatible_states(state1, state2, acceptance_pos):
    if acceptance_pos in state1 and acceptance_pos in state2:
        return True
    elif acceptance_pos not in state1 and acceptance_pos not in state2:
        return True
    else:
        return False
    

def compatible_follow_pos(state1, state2, tree):
    #print('state1: ', state1)
    #print('state2: ', state2)
    f_1 = []
    f_2 = []
    for e in state1:
        f_1.append(tree.searchPos(e).follow_pos)

    for e in state2:
        f_2.append(tree.searchPos(e).follow_pos)

    return f_1 == f_2

    #print('   f_1: ', f_1)
    #print('   f_2: ', f_2)
    #print('   f_1 == f_2: ', f_1 == f_2)




def direct_build(tree, sigma, postfix):
    #print('Mortarion')
    #tree.post2()
    #print('Posición de aceptación: ', tree.searchByVal('#'))
    acceptance_pos = tree.searchByVal('#')
    Dtran = []
    Dstates = []
    Dstates.append(tree.first_pos)
    Marked = []



    # mientras exista un estado no marcado, se procede a marcarlo
    #while Marked != Dstates:
    #    e = next(s for s in Dstates if s not in Marked)
    for e in Dstates:
        #print('e: ', e)
        if e not in Marked:
            Marked.append(e)
            # se obtiene el conjunto de estados alcanzables
            # con cada uno de los símbolos del regex
            #i = 0
            #while i < len(postfix):
            # print('   postfix: ', postfix)
            for i in range(len(postfix)):
                acu = []
                #print('   i: ', postfix[i])
                if postfix[i] in sigma:
                    if (i+1) in e:
                        #print(i+1, e)
                        #print(tree.searchPos(i+1).val)
                        #print(tree.searchPos(i+1).follow_pos)
                        #acu.append(tree.searchPos(i+1).follow_pos)
                        """temp_awedowed = tree.searchPos(i+1).follow_pos
                        print("temp_awedowed: ", temp_awedowed)
                        for e2 in temp_awedowed:
                            if e2 not in acu:
                                acu.append(e2)"""
                        acu = tree.searchPos(i+1).follow_pos
                        #print(acu)

                        # comprobar que no existas dos transiciones con el mismo símbolo
                        # en el mismo estado
                        # si existe, se concatena el conjunto de estados alcanzables
                        # de la transición existente con el nuevo conjunto de estados
                        # alcanzables
                        for t in Dtran:
                            if t[0] == e and t[1] == postfix[i]:
                                #t[2] = t[2] + acu
                                for e2 in acu:
                                    if e2 not in t[2]:
                                        t[2].append(e2)
                                acu = t[2]

                        # se determina si el nuevo conjunto de estados alcanzables
                        # ya existe en Dstates, si no existe, se agrega a Dstates
                        #if acu not in Dstates:
                        if acu not in Dstates:
                            #Dstates.append(acu)
                            for e2 in Dstates:
                                #print('e2: ', e2)
                                #print('acu: ', acu)
                                if ArrayInArray(acu, e2):
                                    # también se debe validar que los estados sean compatibles:
                                    # Con esto, me refiero a que si un estado tiene un símbolo que lo vuelva de aceptación
                                    # y otro que no, entonces no son compatibles y no se pueden unir
                                    if compatible_states(acu, e2, acceptance_pos):
                                        # Otro aspecto a considerar es que si dos estados tienen el mismo follow_pos
                                        # entonces se pueden unir
                                        if compatible_follow_pos(acu, e2, tree):
                                            acu = e2                                    
                            Dstates.append(acu)
                            """for j in Dstates:
                                if not ArrayInArray(acu, j):
                                    #acu = j
                                    Dstates.append(acu)
                                else:
                                    acu = j
                        else:
                            acu = next(s for s in Dstates if s == acu)"""
                        # se crea la transición
                        
                        """if ArrayInArray(acu, e):
                            #temp = [e, e, postfix[i]]
                            # Osea que la transición es a si mismo
                            temp = [e, postfix[i], e]
                        else:
                            #temp = [e, acu, postfix[i]]
                            temp = [e, postfix[i], acu]"""
                        
                        temp = [e, postfix[i], acu]
                        if temp not in Dtran:
                            Dtran.append(temp)

    #print("Dtran: ", Dtran)
    
    direct_states = []
    i = 0
    for e in Marked:
        direct_states.append(state(f"S{i}",e))
        i += 1

    # determinar los estados de aceptación
    for e in direct_states:
        if (len(postfix)+1) in e.contains:
            e.isAccept = True



    for e in Dtran:
        for e2 in direct_states:
            if e[0] == e2.contains:
                for e3 in direct_states:
                    if e[2] == e3.contains:
                        #print(e[0], '|', e2.name, '-' , e[1], '->', e3.name)
                        e2.addTransition(e[1], e3)
    
    return direct_states

def visual_directAFD(AFD, exp):
    g = graphviz.Digraph(comment='direct_AFD', format='png')
    g.attr('node', shape='circle')
    g.attr('node', style='filled')
    g.attr('node', color='lightblue2')
    g.attr('node', fontcolor='black')
    g.attr('edge', color='black')
    g.attr('edge', fontcolor='black')
    g.attr('edge', fontsize='20')
    g.attr('graph', rankdir='LR')
    g.attr('graph', size='17')
    
    g.attr(label = exp)


    for e in AFD:
        if e.isAccept:
            g.node(e.name, e.name, shape='doublecircle')
        else:
            g.node(e.name, e.name)
        for k, v in e.transitions.items():
            if v != None:
                g.edge(e.name, v.name, label=k)
    g.render('direct_AFD', view=True, directory='./visual_results/') 


