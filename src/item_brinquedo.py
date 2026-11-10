"""
    Módulo de especialização de brinquedos do sistema Open Hands.

    Define a classe concreta ItemBrinquedo, derivada da classe abstrata Item,
    destinada ao gerenciamento de brinquedos para doação a orfanatos e casas de apoio,
    com controle da condição de conservação do produto.
"""

try: # ALTERADO: funciona como pacote (app/item_brinquedo.py) ou com os arquivos na mesma pasta
    from .item import Item
except ImportError:
    from item import Item

class ItemBrinquedo(Item):
    """
    Representa um donativo da categoria brinquedo no sistema.

    Especializa a classe base Item incorporando uma escala de conservação (0 a 10)
    para qualificar o estado físico do brinquedo antes de ser direcionado às instituições.
    """

    def __init__(self, nome: str, quantidade: int, descricao: str, estado: int):
        super().__init__(nome, quantidade, descricao)# Atributos herdados da classe Item
        self.estado = estado # Nível de conservação do item em uma escala inteira de 0 a 10.

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor: int):
        """
        Define e valida a nota de conservação do brinquedo.

        Args:
            valor: Número inteiro entre 0 (muito desgastado) e 10 (novo/ótimo estado).

        Raises:
            ValueError: Se o valor não for um inteiro ou estiver fora do intervalo de 0 a 10.
        """
        if type(valor) is not int or not 0 <= valor <= 10: # ALTERADO: type() no lugar de isinstance(), porque True é um int em Python e passaria
            raise ValueError("Valor invalido, insira um numero de 0 a 10")
        self.__estado = valor

    def exibir_detalhes(self):
        """
        Formata e retorna as informações completas do brinquedo.

        Sobrescreve o método abstrato herdado de Item para incorporar a nota de
        conservação na formatação textual do donativo.

        Returns:
            str: Informações estruturadas contendo nome, quantidade, estado e descrição.
        """
        # ALTERADO: mesmo formato nas cinco classes (linhas sem espaço no início e com espaço depois de "Descrição:")
        return (f"Item: {self.nome}\n"
                f"Quantidade: {self.quantidade}\n"
                f"Estado: {self.estado}/10\n"
                f"Descrição: {self.descricao}")
