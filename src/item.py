"""
    Módulo responsável pela definição do modelo base de itens do sistema Open Hands.

    Define a classe abstrata Item, que estabelece os atributos e comportamentos
    comuns para todas as categorias de itens a serem doados.
"""
from abc import ABC, abstractmethod

class Item(ABC):

"""
    Classe base abstrata que representa um item ou donativo no sistema.

    Reúne os atributos e validações compartilhados por todas as categorias
    especializadas de itens (como alimentos, roupas, brinquedos, rações e produtos
    de higiene), garantindo integridade dos dados e padronização por meio de herança.
"""

    def __init__(self, nome: str, quantidade: int, descricao: str):
"""
    Inicializa uma instância da classe base Item[cite: 3].

    A atribuição direta às propriedades dispara os respectivos setters,
    garantindo a validação dos parâmetros logo na criação do objeto.
"""
        self.nome = nome # Nome do item/produto doado ou solicitado.
        self.quantidade = quantidade # Quantidade de unidades disponíveis ou requeridas.
        self.descricao = descricao # Descrição complementar ou observações do item.

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter #Encapsulamento e validação dos parametros, toranando eles privados e validando quanto ao tiṕo e caso o usuario insira valores vazios
    def nome(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome invalido")
        self.__nome = valor.strip()

    @property
    def quantidade(self):
        return self.__quantidade
    
    @quantidade.setter
    def quantidade(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Valor invalido")
        self.__quantidade = valor

    @property
    def descricao(self):
        return self.__descricao
    
    @descricao.setter
    def descricao(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Valor invalido")
        self.__descricao = valor.strip()

    @abstractmethod
    def exibir_detalhes(self):
        pass
