from abc import ABC, abstractmethod

class Item(ABC):

    def __init__(self, nome: str, quantidade: int, descricao: str):
        self.nome = nome
        self.quantidade = quantidade
        self.descricao = descricao

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
