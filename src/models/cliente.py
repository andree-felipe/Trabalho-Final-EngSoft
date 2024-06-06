import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pickle
import os.path

class Cliente():
    def __init__(self, nome, endereco, email, cpf):
        self.__nome = nome
        self.__endereco = endereco
        self.__email = email
        self.__cpf = cpf

    @property
    def nome(self):
        return self.__nome

    @property
    def endereco(self):
        return self.__endereco
 
    @property
    def email(self):
        return self.__email 
    
    @property
    def cpf(self):
        return self.__cpf
    
    
class LimiteCadastroCliente(tk.Toplevel):
    def __init__(self, controle):

        # Esse limite pertence a um limite superior
        tk.Toplevel.__init__(self)
        self.controle = controle 
        self.geometry('250x150')
        self.title('Cdastrar Cliente')

        # Frames
        self.frameNome = tk.Frame(self)
        self.frameEndereco = tk.Frame(self)
        self.frameEmail = tk.Frame(self)
        self.frameCPF = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        # Packs dos frames
        self.frameNome.pack()
        self.frameEndereco.pack()
        self.frameEmail.pack()
        self.frameCPF.pack()
        self.frameButton.pack()
        
        # Input Nome
        self.labelNome = tk.Label(self.frameNome, text='Nome do cliente:')
        self.labelNome.pack(side='left')
        self.inputNome = tk.Entry(self.frameNome, width=20)
        self.inputNome.pack(side='left')

        # Input Endereço
        self.labelEndereco = tk.Label(self.frameEndereco, text='Endereço:')
        self.labelEndereco.pack(side='left')
        self.inputEndereco = tk.Entry(self.frameEndereco, width=20)
        self.inputEndereco.pack(side='left')

        # Input Email
        self.labelEmail = tk.Label(self.frameEmail, text='Email:')
        self.labelEmail.pack(side='left')
        self.inputEmail = tk.Entry(self.frameEmail, width=20)
        self.inputEmail.pack(side='left')

        # Input CPF
        self.labelCPF = tk.Label(self.frameCPF, text='CPF: ')
        self.labelCPF.pack(side='left')
        self.inputCPF = tk.Entry(self.frameCPF, width=20)
        self.inputCPF.pack(side='left')
        
        # Botão para cadastrar
        self.buttonCadastra = tk.Button(self.frameButton, text='Cadastrar')
        self.buttonCadastra.pack(side='left')
        self.buttonCadastra.bind('<Button>', controle.cadastraHandler)
        
        # Botão para limpar campos preenchidos
        self.buttonLimpa = tk.Button(self.frameButton, text='Limpar')
        self.buttonLimpa.pack(side='left')
        self.buttonLimpa.bind('<Button>', controle.limpaHandler)

        # Botão para fechar a janela
        self.buttonFecha = tk.Button(self.frameButton, text='Concluído')
        self.buttonFecha.pack(side='left')
        self.buttonFecha.bind('<Button>', controle.fechaHandler)
        
    # Método para mostrar uma janela com mensagem
    def mostraJanela(Self, titulo, msg):
        messagebox.showinfo(titulo, msg)
        

class CtrlCliente():
    def __init__(self):
        
        # Verificação arquivo pickle com lista de clientes
        if not os.path.isfile('clientes.pickle'):
            self.listaClientes = []
        else:
            with open('clientes.pickle', 'rb') as f:
                self.listaClientes = pickle.load(f)
        
    # Método para criação do limite (janela) do cadastro de clientes
    def cadastraCliente(self):
        self.limiteCadastraCliente = LimiteCadastroCliente(self)
        
    # Callback de cadastro de um cliente (botão cadastrar)
    def cadastraHandler(self, event):
        nome = self.limiteCadastraCliente.inputNome.get()
        endereco = self.limiteCadastraCliente.inputEndereco.get()
        email = self.limiteCadastraCliente.inputEmail.get()
        cpf = int(self.limiteCadastraCliente.inputCPF.get())
        clt = Cliente(nome, endereco, email, cpf)
        aux = False
        for clt in self.listaClientes:
            if cpf == clt.cpf:
                aux = True
                self.limiteCadastraCliente.mostraJanela('Erro', 'CPF já cadastrado')
                self.limpaHandler(event)
            break
        if not aux:
            self.listaClientes.append(clt)
            if len(self.listaClientes) != 0:
                with open('clientes.pickle', 'wb') as f:
                    pickle.dump(self.listaClientes, f)
            self.limiteCadastraCliente.mostraJanela('Sucesso', 'Cliente cadastrado')
            self.limpaHandler(event)

    # Callback de limpeza daos inputs após cadastro 
    def limpaHandler(self, event):
        self.limiteCadastraCliente.inputNome.delete(0, len(self.limiteCadastraCliente.inputNome.get()))
        self.limiteCadastraCliente.inputEndereco.delete(0, len(self.limiteCadastraCliente.inputEndereco.get()))
        self.limiteCadastraCliente.inputEmail.delete(0, len(self.limiteCadastraCliente.inputEmail.get()))
        self.limiteCadastraCliente.inputCPF.delete(0, len(self.limiteCadastraCliente.inputCPF.get()))
        
    # Método para fechar o limite (janela) de cadastro de um cliente (botão fechar)
    def fechaHandler(self, event):
        self.limiteCadastraCliente.destroy()

    # Método para consultar as informações de um cliente
    def consultarCliente(self):
        msg = ''
        cpfParam = simpledialog.askinteger('Consulta de Cliente', 'Insira o CPF do cliente: ')
        aux = False
        for cliente in self.listaClientes:
            if cpfParam == int(cliente.cpf):
                aux = True
                msg += 'Nome: ' + cliente.nome + '\n'
                msg += 'Endereço: ' + cliente.endereco + '\n'
                msg += 'Email: ' + cliente.email + '\n'
                messagebox.showinfo('Cliente encontrado', msg)
            break
        if not aux:
            messagebox.showinfo('Erro', 'Não há cliente com esse CPF')
            
    # Método de instanciação para controladores externos
    def getListaClientes(self):
        return self.listaClientes
            