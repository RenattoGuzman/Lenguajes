#file = './tests/slr-1.yal'

from yalex import grammar, generate_alphabet, parser
from InfixToPostfix import *
from BinaryTree import *
from direct_AFD import direct_build, visual_directAFD
import time

files = [
    './tests/slr-1.yal',
    './tests/slr-2.yal',
    './tests/slr-3.yal',
    './tests/slr-4.yal'
]

#file = files[1]


def main(file):
    print('-------------------------------------------------------------')    

    l, r = grammar(file)
    sigma, regex = generate_alphabet(l, r)

    print('Vex\'ahlia Vessar')
    print('-------------------------------------------------------------')


    for e in l:
        print(e, ' = ', l[e])

    print('Cassandra de Rolo')
    print('-------------------------------------------------------------')

    for e in r:
        print(e, ' = ', r[e])

    print('\nPercival Frederickstein von Musel Klossowski de Rolo III')
    print('-------------------------------------------------------------')


    print('Alfabeto: ', sigma)
    print('Expresion regular: ', regex)

    print('-------------------------------------------------------------')


    r, sigma = parser(regex, l, sigma)

    r_string = ''.join(r)

    #print('Array regex: ', r)
    print('Expresion regular: ', r_string)
    print('Keyleth')
    print('--------------------------------------------------------.-----')

    

    postfix = InfixToPostfix(r)

    print('Expresion regular postfija: ', ''.join(postfix))

    print('-'*60)

    

    postfix.append('#')
    postfix.append("'.'")

    tree = buildTree(postfix.pop(), postfix)

    visual_tree = tree.generate_graph()
    tree.traversePostOrder()
    #tree.post2()
    #tree.determineFollowPos()
    #tree.post3()
    
    sigma = []
    for e in postfix:
        if e not in operators and e not in sigma and e != 'ε':
            sigma.append(e)
    
    AFD_directo = direct_build(tree, sigma, postfix)
    print(f"\n\n==>> AFD_directo: \n{AFD_directo}\n\n")
    visual_directAFD(AFD_directo, "1")

    print('-------------------------------------------------------------')

    #visual_tree.render(file, view=True, format='png', cleanup=True, directory='./visual/', quiet=True)

for file in files:
    main(file)
    # make the program wait for some seconds
    time.sleep(3)

#main(files[2])