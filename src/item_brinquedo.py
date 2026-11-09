from .item import Item

class ItemBrinquedo(Item):

    def __init__(self, nome: str, quantidade: int, descricao: str, estado: int):
        super().__init__(nome, quantidade, descricao)
        self.estado = estado

    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor: int):
        if not isinstance(valor, int) or not 0 <= valor <= 10:
            raise ValueError("Valor invalido, insira um numero de 0 a 10")
        self.__estado = valor

    def exibir_detalhes(self):
        return(f"Item: {self.nome}\n Quantidade: {self.quantidade}\n Estado: {self.estado}/10\n Descrição:{self.descricao}")
