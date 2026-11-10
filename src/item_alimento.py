
"""
    Módulo de especialização de itens alimentícios do sistema Open Hands.
 
    Define a classe concreta ItemAlimento, derivada da classe abstrata Item,
    incorporando controle de prazos de validade e descarte de produtos vencidos.
"""
 
from datetime import date
try: # ALTERADO: funciona como pacote (app/item_alimento.py) ou com os arquivos na mesma pasta
    from .item import Item, converter_data # ALTERADO: importa também converter_data
except ImportError:
    from item import Item, converter_data
 
class ItemAlimento(Item):
    """
    Representa um item do tipo alimento destinado a doações.
 
    Especializa a classe base Item adicionando o controle da data de validade
    para garantir a segurança alimentar dos beneficiários atendidos pelo sistema.
    """
 
    def __init__(self, nome: str, quantidade: int, descricao: str, validade: date):
        super().__init__(nome, quantidade, descricao) #Herança dos atributos da classe mãe Item
        self.validade = validade #Data de validade (deve ser posterior ou igual à data atual)
 
    @property
    def validade(self):
        return self.__validade
 
    @validade.setter
    def validade(self, valor): # ALTERADO: sem a dica de tipo date, porque agora aceita também texto
        """
        Define e valida a data de validade do alimento.
 
        Args:
             valor: Objeto date ou texto (DD/MM/AAAA ou AAAA-MM-DD) contendo a validade do produto.
 
        Raises:
             ValueError: Se o valor não for uma data válida ou se a data for anterior à data atual.
        """
        valor = converter_data(valor) # ALTERADO: converte texto em date e recusa o que não for data (antes: isinstance(valor, date))
        if valor < date.today():
            raise ValueError("Nao aceitamos alimentos vencidos")
        self.__validade = valor
 
    def exibir_detalhes(self):
        """
        Formata e retorna as informações detalhadas do alimento.
 
        Sobrescreve o método abstrato herdado de Item para incluir a exibição
        formatada da data de validade (DD/MM/AAAA) junto aos atributos base.
 
        Returns:
            str: String formatada contendo nome, quantidade, validade e descrição.
        """
        # ALTERADO: mesmo formato nas cinco classes (linhas sem espaço no início e com espaço depois de "Descrição:")
        return (f"Item: {self.nome}\n"
                f"Quantidade: {self.quantidade}\n"
                f"Validade: {self.validade.strftime('%d/%m/%Y')}\n"
                f"Descrição: {self.descricao}")
