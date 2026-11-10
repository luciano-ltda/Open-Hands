"""
    Módulo responsável pela definição do modelo base de itens do sistema Open Hands.

    Define a classe abstrata Item, que estabelece os atributos e comportamentos
    comuns para todas as categorias de itens a serem doados.
"""
from abc import ABC, abstractmethod
from datetime import date, datetime # NOVO: usados pela função converter_data


def converter_data(valor): # NOVO: função usada pelas classes que têm validade (alimento, higiene e ração)
    """
    Converte o valor recebido em um objeto date.

    Aceita um date ou um texto em DD/MM/AAAA ou AAAA-MM-DD, que é como a data
    chega de um campo da interface.

    Args:
        valor: Objeto date ou texto contendo a data.

    Returns:
        date: A data convertida.

    Raises:
        ValueError: Se o valor não for um date nem um texto em um dos formatos aceitos.
    """
    if type(valor) is date: # Já é um date: devolve como está (type() recusa datetime, que quebraria a comparação com date.today())
        return valor
    if isinstance(valor, str): # Texto: tenta cada formato aceito
        texto = valor.strip()
        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError: # Não bateu com esse formato, tenta o próximo
                pass
    raise ValueError("Insira uma data valida (DD/MM/AAAA)")


class Item(ABC):
    """
    Classe base abstrata que representa um item ou donativo no sistema.

    Reúne os atributos e validações compartilhados por todas as categorias
    especializadas de itens (como alimentos, roupas, brinquedos, rações e produtos
    de higiene), garantindo integridade dos dados e padronização por meio de herança.
    """

    def __init__(self, nome: str, quantidade: int, descricao: str):
        """
        Inicializa uma instância da classe base Item.

        A atribuição direta às propriedades dispara os respectivos setters,
        garantindo a validação dos parâmetros logo na criação do objeto.
        """
        self.nome = nome # Nome do item/produto doado ou solicitado.
        self.quantidade = quantidade # Quantidade de unidades disponíveis ou requeridas.
        self.descricao = descricao # Descrição complementar ou observações do item.

    @property
    def nome(self):
        return self.__nome

    @nome.setter #Encapsulamento e validação dos parametros, tornando eles privados e validando quanto ao tipo e caso o usuario insira valores vazios
    def nome(self, valor: str):
        """
        Define e valida o nome do item.

        Args:
            valor: Texto contendo o nome do item.

        Raises:
            ValueError: Se o valor não for uma string ou contiver apenas espaços.
        """
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome invalido")
        self.__nome = valor.strip()

    @property
    def quantidade(self):
        return self.__quantidade

    @quantidade.setter
    def quantidade(self, valor: int):
        """
        Define e valida a quantidade do item.

        Args:
            valor: Quantidade inteira a ser registrada.

        Raises:
            ValueError: Se o valor não for um número inteiro ou for menor/igual a zero.
        """
        if type(valor) is not int or valor <= 0: # ALTERADO: type() no lugar de isinstance(), porque True é um int em Python e passaria
            raise ValueError("Valor invalido")
        self.__quantidade = valor

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, valor: str):
        """
        Define e valida a descrição do item.

        Args:
            valor: Texto contendo as características do item.

        Raises:
            ValueError: Se o valor não for uma string ou contiver apenas espaços.
        """
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Valor invalido")
        self.__descricao = valor.strip()

    @abstractmethod
    def exibir_detalhes(self):
        """
        Exibe as informações detalhadas e específicas do item no terminal/interface.

        Método abstrato que força a implementação polimórfica nas classes
        filhas (ex.: ItemAlimento, ItemRoupa, ItemRacao), permitindo que cada
        uma apresente seus atributos exclusivos.
        """
        pass
