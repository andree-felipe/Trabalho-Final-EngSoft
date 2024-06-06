import tkinter as tk
from tkinter import messagebox
from models import estoque as estoque
from models import venda as venda
from models import cliente as cliente
from models import faturamento as faturamento

class LimitePrincipal():
    def __init__(self, root, controle):
        self.controle = controle
        
        # Raiz da aplicação
        self.root = root
        self.root.geometry('300x100')

        # Instância de barra de menu e os submenus
        self.menubar = tk.Menu(self.root)        
        self.estoqueMenu = tk.Menu(self.menubar)    
        self.vendaMenu = tk.Menu(self.menubar)
        self.clienteMenu = tk.Menu(self.menubar)
        self.faturamentoMenu = tk.Menu(self.menubar)   

        # Métodos e cascata do submenu Estoque
        self.estoqueMenu.add_command(label="Cadastrar mercadoria", command=self.controle.cadastrarMercadoria)
        self.estoqueMenu.add_command(label='Consultar mercadoria', command=self.controle.consultarMercadoria)
        self.menubar.add_cascade(label="Estoque", menu=self.estoqueMenu)
        
        # Métodos e cascata do submenu Cliente
        self.clienteMenu.add_command(label='Cadastrar cliente', command=self.controle.cadastrarCliente)
        self.clienteMenu.add_command(label='Consultar cliente', command=self.controle.consultarCliente)
        self.menubar.add_cascade(label='Cliente', menu=self.clienteMenu)
        
        # Métodos e cascata do submenu Venda
        self.vendaMenu.add_command(label="Emitir Nota Fiscal", command=self.controle.emitirNotaFiscal)
        self.menubar.add_cascade(label="Venda", menu=self.vendaMenu)
        
        # Métodos e cascata do submenu Faturamento
        self.faturamentoMenu.add_command(label='Consultar faturamento por cliente', command=self.controle.consultarFatCPF)
        self.faturamentoMenu.add_command(label='Consultar faturamento por produto', command=self.controle.consultarFatCod)
        self.menubar.add_cascade(label='Faturamento', menu=self.faturamentoMenu)
        
        self.root.config(menu=self.menubar)
          

class ControlePrincipal():
    def __init__(self):
        self.root = tk.Tk()

        self.ctrlEstoque = estoque.CtrlEstoque()
        self.ctrlVenda = venda.CtrlVenda(self)
        self.ctrlCliente = cliente.CtrlCliente()
        self.ctrlFaturamento = faturamento.CtrlFaturamento(self)

        self.limite = LimitePrincipal(self.root, self) 

        self.root.title("Loja de Confecções")
        
        #inicia o mainloop
        self.root.mainloop()

    def cadastrarMercadoria(self):
        self.ctrlEstoque.cadastraMercadoria()
        
    def consultarMercadoria(self):
        self.ctrlEstoque.consultarMercadoria()

    def cadastrarCliente(self):
        self.ctrlCliente.cadastraCliente()
        
    def consultarCliente(self):
        self.ctrlCliente.consultarCliente()
        
    def emitirNotaFiscal(self):
        self.ctrlVenda.emitirNota()
        
    def consultarFatCPF(self):
        self.ctrlFaturamento.consultarFatCliente()
        
    def consultarFatCod(self):
        self.ctrlFaturamento.consultarFatProduto()           

if __name__ == "__main__":
    c = ControlePrincipal() 