import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from yalex import grammar, generate_alphabet, parser, PreprocessEntry, updateSigma
from InfixToPostfix import *
from BinaryTree import *
import time
from AFN import *
from direct_AFD import *


class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de AFD")
        self.root.configure(bg='#FC7A1E')  # Color de fondo para la raíz

        self.style = ttk.Style()

        # Creamos un estilo personalizado para los Frames
        self.style.configure('Custom.TFrame', background='#FC7A1E') 
         
        self.style.configure('TButton', background='#053225', foreground='#053225', font=('Arial', 12, 'bold'))
        self.style.configure('TLabel', background='#053225', foreground='#FFFFFF', font=('Arial', 18, 'bold'))

        self.frame = ttk.Frame(self.root, style='Custom.TFrame')  # Usamos el estilo personalizado
        self.frame.pack(pady=10)

        self.text_label = ttk.Label(self.frame, text="Texto:", padding=(10, 5))
        self.text_label.grid(row=0, column=0, sticky="w")

        self.text_box = ScrolledText(self.frame, width=90, height=10, font=('Arial', 12), bg='#8BAAAD')
        self.text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.generate_button = ttk.Button(self.frame, text="Generar AFD", command=self.generate_afd)
        self.generate_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.result_label = ttk.Label(self.root, text="Resultados:", padding=(10, 5))
        self.result_label.pack()

        self.results_text = ScrolledText(self.root, width=90, height=10, font=('Arial', 12), bg='#8BAAAD')
        self.results_text.pack(pady=10)


    def generate_afd(self):
        input_text = self.text_box.get("1.0", "end-1c")  

        print('-------------------------------------------------------------')    

        l, r = grammar(input_text)
        sigma, regex = generate_alphabet(l, r)

        print('-------------------------------------------------------------')


        for e in l:
            print(e, ' = ', l[e])

        print('-------------------------------------------------------------')

        for e in r:
            print(e, ' = ', r[e])

        print('-------------------------------------------------------------')


        print('Alfabeto: ', sigma)
        print('Expresion regular: ', regex)

        print('-------------------------------------------------------------')


        r, sigma = parser(regex, l, sigma)

        r_string = ''.join(r)

        print('Expresion regular: ', r_string)
        print('--------------------------------------------------------.-----')

        

        tratemos = InfixToPostfix(r)
        postfix_copia = tratemos.copy()
        updateSigma(r, sigma)

        print('Expresion regular postfija: ', ''.join(tratemos))
        print('Alfabeto: ', sigma)

        print('-'*60)

        

        tratemos.append('#')
        tratemos.append("'.'")

        tree = buildTree(tratemos.pop(), tratemos)

        tree.traversePostOrder()
        

        tree.determineFollowPos()

        AFD_directo = direct_build(tree, sigma, postfix_copia)
        visual_directAFD(AFD_directo, ''.join(regex))

        print('-------------------------------------------------------------')
        
        # For demonstration purposes, let's just display the input text as a result
        self.results_text.delete("1.0", "end")  # Clear previous results
        self.results_text.insert("end", input_text)

def mainInterfaz():
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()

if __name__ == "__main__":
    mainInterfaz()

