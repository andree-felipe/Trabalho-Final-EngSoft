import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pickle
import os.path

class Mercadoria():
    def __init__(self, codigoNumerico, descricao, precoCompra, valorVenda, quant):
        self.__codigoNumerico = codigoNumerico
        self.__descricao = descricao
        self.__precoCompra = precoCompra
        self.__valorVenda = valorVenda
        self.__quant = quant

    @property
    def codigoNumerico(self):
        return self.__codigoNumerico

    @property
    def descricao(self):
        return self.__descricao
 
    @property
    def precoCompra(self):
        return self.__precoCompra 
    
    @property
    def valorVenda(self):
        return self.__valorVenda
    
    @property
    def quant(self):
        return self.__quant
    
    @quant.setter
    def quantidad(self, quant):
        self.__quant = quant

class LimiteCadastroMercadoria(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('280x150')
        self.title("Cadastrar Mercadoria")
        self.controle = controle

        # Frames das informações
        self.frameCodigo = tk.Frame(self)
        self.frameDescricao = tk.Frame(self)
        self.framePrecoCompra = tk.Frame(self)
        self.frameValorVenda = tk.Frame(self)
        self.frameQuant = tk.Frame(self)
        self.frameEspacamento = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        
        # Pack dos frames
        self.frameCodigo.pack()
        self.frameDescricao.pack()
        self.framePrecoCompra.pack()
        self.frameValorVenda.pack()
        self.frameQuant.pack()
        self.frameEspacamento.pack()
        self.frameButton.pack()
      
        self.labelCodigo = tk.Label(self.frameCodigo,text="Código: ")
        self.labelCodigo.pack(side="left")

        self.inputCodigo = tk.Entry(self.frameCodigo, width=20)
        self.inputCodigo.pack(side="left")

        self.labelDescricao = tk.Label(self.frameDescricao,text="Descrição: ")
        self.labelDescricao.pack(side="left")

        self.inputDescricao = tk.Entry(self.frameDescricao, width=20)
        self.inputDescricao.pack(side="left")

        self.labelPrecoCompra = tk.Label(self.framePrecoCompra,text="Preço de compra: ")
        self.labelPrecoCompra.pack(side="left")  

        self.inputPrecoCompra = tk.Entry(self.framePrecoCompra, width=20)
        self.inputPrecoCompra.pack(side="left")

        self.labelValorVenda = tk.Label(self.frameValorVenda,text="Valor de Venda: ")
        self.labelValorVenda.pack(side="left")  

        self.inputValorVenda = tk.Entry(self.frameValorVenda, width=20)
        self.inputValorVenda.pack(side="left")  
        
        self.labelQuant = tk.Label(self.frameQuant, text='Quantidade: ')           
        self.labelQuant.pack(side='left')

        self.inputQuant = tk.Entry(self.frameQuant, width=20)
        self.inputQuant.pack(side='left')
        
        self.labelEspacamento = tk.Label(self.frameEspacamento)
        self.labelEspacamento.pack(side='left')
      
        self.buttonSubmit = tk.Button(self.frameButton ,text="Enter")      
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.enterHandlerCadastro)
      
        self.buttonClear = tk.Button(self.frameButton ,text="Clear")      
        self.buttonClear.pack(side="left")
        self.buttonClear.bind("<Button>", controle.clearHandlerCadastro)  

        self.buttonFecha = tk.Button(self.frameButton ,text="Concluído")      
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.closeHandlerCadastro)

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)


class CtrlEstoque():
    def __init__(self):
        
        #verificação arquivo pickle com controle de estoque
        if not os.path.isfile('estoque.pickle'):
            self.listaProdutos = []
        else:
            with open('estoque.pickle', 'rb') as f:
                self.listaProdutos = pickle.load(f)
                
    # Método de criação do limite (janela) para cadastrar uma mercadoria
    def cadastraMercadoria(self):
        self.limiteCadastro = LimiteCadastroMercadoria(self)

    # Callback de cadastro de produto (botão cadastrar)
    def enterHandlerCadastro(self, event):
        # Coletando informações dos inputs
        codigo = int(self.limiteCadastro.inputCodigo.get())
        descricao = self.limiteCadastro.inputDescricao.get()
        precoCompra = int(self.limiteCadastro.inputPrecoCompra.get())
        valorVenda = int(self.limiteCadastro.inputValorVenda.get())
        quant = int(self.limiteCadastro.inputQuant.get())
        
        # Verificação no estoque
        for produto in self.listaProdutos:
            if produto.codigoNumerico == codigo:
                if produto.descricao == descricao:
                    if produto.precoCompra == precoCompra:
                        if produto.valorVenda == valorVenda:
                            # Se todas informações forem iguais a de um produto já cadastrado, atualiza a quantidade em estoque
                            produto.quant += int(quant)
                            print(produto.quant)
                            self.limiteCadastro.mostraJanela('Produto já cadastrado', 'Estoque atualizado')
                            self.clearHandlerCadastro(event)
                else:
                    # Descrição da mercadoria igual a de alguma outra já cadastrada
                    self.limiteCadastro.mostraJanela('Erro', 'Já existe outro produto com essa descrição')
                    self.clearHandlerCadastro(event)
            else:
                # Código da mercadoria igual a de alguma outra já cadastrada
                self.limiteCadastro.mostraJanela('Erro', 'Já existe outro produto com esse código')
                self.clearHandlerCadastro(event)
                
        # Instânciando uma mercadoria
        novaMercadoria = Mercadoria(codigo, descricao, precoCompra, valorVenda, quant)
        self.listaProdutos.append(novaMercadoria)
        self.limiteCadastro.mostraJanela("Sucesso", "Produto cadastrado!")
        self.clearHandlerCadastro(event)

    # Método para limpeza dos inputs preenchidos
    def clearHandlerCadastro(self, event):
        self.limiteCadastro.inputCodigo.delete(0, len(self.limiteCadastro.inputCodigo.get()))
        self.limiteCadastro.inputDescricao.delete(0, len(self.limiteCadastro.inputDescricao.get()))
        self.limiteCadastro.inputPrecoCompra.delete(0, len(self.limiteCadastro.inputPrecoCompra.get()))
        self.limiteCadastro.inputValorVenda.delete(0, len(self.limiteCadastro.inputValorVenda.get()))
        self.limiteCadastro.inputQuant.delete(0, len(self.limiteCadastro.inputQuant.get()))

    # Callback para fechar a janela e persistir informações no sistema (botão concluído)
    def closeHandlerCadastro(self, event):
        if len(self.listaProdutos) != 0:
            # Persistindo dados
            with open('estoque.pickle', 'wb') as f:
                pickle.dump(self.listaProdutos, f)
        self.limiteCadastro.destroy()

    # Callback para consultar unma mercadoria (submenu: consultar mercadoria)
    def consultarMercadoria(self):
        msg = ''
        codigoParametro = simpledialog.askinteger('Consulta de Mercadoria', 'Insira o código da mercadoria: ')
        aux = False
        
        for prod in self.listaProdutos:
            if codigoParametro == int(prod.codigoNumerico):
                aux = True
                msg += 'Estoque: ' + str(prod.quant) + '\n'
                msg += 'Descrição: ' + prod.descricao + '\n'
                msg += 'Preço de compra: ' + str(prod.precoCompra) + '\n'
                msg += 'Preço de venda: ' + str(prod.valorVenda) + '\n'
        
        if not aux:
            messagebox.showinfo('Erro', 'Não há mercadoria com esse código')
            return
        
        messagebox.showinfo('Mercadoria encontrada', msg)
        
    
    def atualizaEstoque(self, listaProdutos):
            with open('estoque.pickle', 'wb') as f:
                pickle.dump(listaProdutos, f)
    
    # Método para instancias uma mercadoria
    def criaMercadoria(self, codigo, descricao, precoCompra, valorVenda, quant):
        prodRet = None
        prodRet = Mercadoria(codigo, descricao, precoCompra, valorVenda, quant)
        return prodRet

    # Método de instanciação para controladores externos
    def getListaProdutos(self):
        return self.listaProdutos