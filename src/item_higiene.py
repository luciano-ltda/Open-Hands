"""
    Módulo de especialização de itens de higiene do sistema Open Hands.

    Define a classe concreta ItemHigiene, derivada da classe abstrata Item,
    incorporando controle de prazos de validade e descarte de produtos vencidos.
"""

from datetime import date
from .item import Item

class ItemHigiene(Item):
"""
    Representa um item do tipo higiene destinado a doações.

    Especializa a classe base Item adicionando o controle da data de validade
"""
    def __init__(self, nome: str, quantidade: int, descricao: str, validade: str):
        super().__init__(nome, quantidade, descricao) #Herança dos atributos da classe mãe Item
        self.validade = validade #Data de validade (deve ser posterior ou igual à data atual)

    @property
    def validade(self):
        return self.__validade
    
    @validade.setter
    def validade(self, valor: date):
"""
    Define e valida a data de validade do produto.

    Args:
         valor: Objeto date contendo a validade do produto.

    Raises:
         ValueError: Se o valor não for uma instância de date ou se a data for anterior à data atual.
"""
        if not isinstance(valor, date):
            raise ValueError("Insira uma data valida")
        if valor <  date.today():
            raise ValueError("Nao aceitamos produtos vencidos")
        self.validade = valor

    def exibir_detalhes(self):

"""
    Formata e retorna as informações detalhadas do produto.

    Sobrescreve o método abstrato herdado de Item para incluir a exibição
    formatada da data de validade (DD/MM/AAAA) junto aos atributos base.

    Returns:
        str: String formatada contendo nome, quantidade, validade e descrição.
"""
        return(f"Item: {self.nome}\n Quantidade: {self.quantidade}\n Validade: {self.validade}\n Descrição:{self.descricao}")
