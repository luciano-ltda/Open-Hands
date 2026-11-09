"""
    Módulo de especialização de vestuário do sistema Open Hands.

    Define a classe concreta ItemRoupa, derivada da classe abstrata Item,
    destinada ao gerenciamento de peças de vestuário e agasalhos para doação,
    com controle de tamanho e índice de conservação da peça.
"""

from .item import Item

class ItemRoupa(Item):
"""
    Representa um donativo da categoria vestuário no sistema.

    Especializa a classe base Item adicionando os atributos específicos de
    tamanho (ex.: P, M, G, 42) e nota de conservação física do tecido.
"""
    def __init__(self, nome: str, quantidade: int, descricao: str, tamanho: str, estado: str):
        super().__init__(nome, quantidade, descricao) # Atributos herdados da classe mae Item
        self.tamanho = tamanho # Tamanho da peça de roupa
        self.estado = estado # Nível de conservação em uma escala inteira de 0 a 10.

    @property
    def tamanho(self):
        return self.__tamanho
    
    @tamanho.setter
    def tamanho(self, valor: str):
"""
    Define e valida o tamanho da peça de roupa.
    Args:
        valor: Identificador do tamanho (ex.: 'P', 'M', 'G', 'GG', '40').
    Raises:
        ValueError: Se o valor não for uma string ou contiver apenas espaços.
"""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Valor invalido")
        self.__tamanho = valor.strip()

    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor: int):
"""
    Define e valida a nota de conservação da peça.
    Args:
        valor: Número inteiro entre 0 (muito desgastada/rasgada) e 10 (nova/excelente).
    Raises:
        ValueError: Se o valor não for um número inteiro ou estiver fora da faixa de 0 a 10.
"""
        if not isinstance(valor, int) or not 0 <= valor <= 10: # valor vai de 0/10 a 10/10 
            raise ValueError("Valor invalido, insira um numero de 0 a 10")
        self.__estado = valor

    def exibir_detalhes(self):
"""
    Formata e retorna as informações estruturadas da peça de roupa.
    Sobrescreve o método abstrato herdado de Item para incorporar as
    especificidades de tamanho e estado de conservação do vestuário.
    Returns:
        str: Detalhes formatados com nome, quantidade, tamanho, estado e descrição.
"""
        return(f"Item: {self.nome}\n Quantidade: {self.quantidade}\n Tamanho: {self.tamanho}\n Estado:{self.estado}/10\n Descrição: {self.descricao}")
