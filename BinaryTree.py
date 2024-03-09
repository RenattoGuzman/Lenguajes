# implementar validación para el símbolo epsilon
import graphviz

class Node:
    def __init__(self, key, right=None, left=None, pos=None):
        self.left = left
        self.right = right
        self.val = key
        self.first_pos = None
        self.last_pos = None
        self.nullable = False
        self.pos = pos
        self.follow_pos = []
        self.accept = False

    def determineNullable(self):
        if self.val == '*':
            self.nullable = True
        elif self.val == "'.'":
            self.nullable = self.left.nullable and self.right.nullable
        elif self.val == '|':
            self.nullable = self.left.nullable or self.right.nullable
        elif self.val == 'ε':
            self.nullable = True
        else:
            self.nullable = False
    
    def determineFirstPos(self):
        if self.val == '*':
            self.first_pos = self.left.first_pos
        elif self.val == "'.'":
            if self.left.nullable:
                self.first_pos = self.left.first_pos + self.right.first_pos
            else:
                self.first_pos = self.left.first_pos
        elif self.val == '|':
            self.first_pos = self.left.first_pos + self.right.first_pos
        elif self.val == 'ε':
            self.first_pos = []
        else:
            self.first_pos = [self.pos]

    def determineLastPos(self):
        if self.val == '*':
            self.last_pos = self.left.last_pos
        elif self.val == "'.'":
            if self.right.nullable:
                self.last_pos = self.left.last_pos + self.right.last_pos
            else:
                self.last_pos = self.right.last_pos
        elif self.val == '|':
            self.last_pos = self.left.last_pos + self.right.last_pos
        elif self.val == 'ε':
            self.last_pos = []
        else:
            self.last_pos = [self.pos]

    def determineFollowPos(self):
        if self.left:
            self.left.determineFollowPos()
            #print(self.left.val, self.left.follow_pos)
        if self.right:
            self.right.determineFollowPos()
            #print(self.right.val, self.right.follow_pos)
        if self.val == "'.'":
            for i in self.left.last_pos:
                self.searchPos(i).follow_pos += self.right.first_pos
                #print( 'i: ', i, 'follow_pos: ', self.right.first_pos)
        elif self.val == '*':
            for i in self.last_pos:
                self.searchPos(i).follow_pos += self.first_pos
                #print( 'i: ', i, 'follow_pos: ', self.first_pos)

    def findi(self, i):
        if self.left:
            self.left.findi(i)
        if self.right:
            self.right.findi(i)
        if self.pos != None:
            i.append(self.pos)
    

    def traversePostOrder(self):
        if self.left:
            self.left.traversePostOrder()
            self.left.determineNullable()
            self.left.determineFirstPos()
            self.left.determineLastPos()
        if self.right:
            self.right.traversePostOrder()
            self.right.determineNullable()
            self.right.determineFirstPos()
            self.right.determineLastPos()
        self.determineNullable()
        self.determineFirstPos()
        self.determineLastPos() 
        if self.val == '#':
            self.accept = True
        #print(self.val if self.val != None else '', end=' ')
        #return self.val if self.val != None else ''
        #print('(', self.first_pos,') - (', self.val if self.val != None else '', '(', self.last_pos,') - (', end=' ')

    def post2(self):
        if self.left:
            self.left.post2()
        if self.right:
            self.right.post2()
        print(self.val, self.nullable, self.pos, self.first_pos, self.last_pos)

    def post3(self):
        if self.left:
            self.left.post3()
        if self.right:
            self.right.post3()
        if self.pos != None:
            print(self.pos, self.val, self.follow_pos, self.accept)
            #return self.pos, self.val, self.follow_pos


    def getNodeByPos(self, pos):
        print(self.val, self.pos)
        if self.left:
            self.left.getNodeByPos(pos)
        if self.right:
            self.right.getNodeByPos(pos)
        if self.pos == pos:
            return self.val

    def search(self, key):
        if self.val == key:
            return self.val
        if self.left:
            if self.left.search(key):
                return self.left.search(key)
        if self.right:
            if self.right.search(key):
                return self.right.search(key)
        return False

    def searchPos(self, pos):
        if self.pos == pos:
            return self
        if self.left:
            if self.left.searchPos(pos):
                return self.left.searchPos(pos)
        if self.right:
            if self.right.searchPos(pos):
                return self.right.searchPos(pos)
        return None
    
    def searchByVal(self, val):
        if self.val == val:
            return self.pos
        if self.left:
            if self.left.searchByVal(val):
                return self.left.searchByVal(val)
        if self.right:
            if self.right.searchByVal(val):
                return self.right.searchByVal(val)
        return None
    
    def generate_graph(self):
        dot = graphviz.Digraph()
        
        def traverse(node):
            if node is None:
                return
            
            dot.node(str(id(node)), label=f'Value: {node.val}\nPosition: {node.pos}\nFirstPos: {node.first_pos}\nLastPos: {node.last_pos}\nFollowPos: {node.follow_pos}')
            
            if node.left:
                traverse(node.left)
                dot.edge(str(id(node)), str(id(node.left)), label='Left')
            
            if node.right:
                traverse(node.right)
                dot.edge(str(id(node)), str(id(node.right)), label='Right')
        
        traverse(self)
        
        return dot


operators = ['*', '|', "'.'"]

#Funcion para determinar si el arreglo a está dentro del arreglo b
def ArrayInArray(a, b):
    r = True
    for e in a:
        if e not in b:
            r = False
    return r

def buildTree(e, exp):
    if e == '*':
        #return Node(e, buildTree(exp[:-1]), None)
        return Node(e, None, buildTree(exp.pop(len(exp)-1), exp))
    elif e == "'.'" or e == '|':
        #
        return Node(e, buildTree(exp.pop(len(exp)-1), exp), buildTree(exp.pop(len(exp)-1), exp))
    else:
        # Una hoja con el símbolo epsilon no debe tener posición
        if e == 'ε':
            return Node(e, None, None)
        else:
            return Node(e, None, None, len(exp)+1)