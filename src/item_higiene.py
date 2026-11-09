from datetime import date

from .item import Item

class ItemHigiene(Item):

    def __init__(self, nome: str, quantidade: int, descricao: str, validade: str):
        super().__init__(nome, quantidade, descricao)
        self.validade = validade

    @property
    def validade(self):
        return self.__validade
    
    @validade.setter
    def validade(self, valor: date):

        if not isinstance(valor, date):
            raise ValueError("Insira uma data valida")
        if valor <  date.today():
            raise ValueError("Nao aceitamos produtos vencidos")
        self.validade = valor

    def exibir_detalhes(self):
        return(f"Item: {self.nome}\n Quantidade: {self.quantidade}\n Validade: {self.validade}\n Descrição:{self.descricao}")
