from .item import Item

class ItemRoupa(Item):

    def __init__(self, nome: str, quantidade: int, descricao: str, tamanho: str, estado: str):
        super().__init__(nome, quantidade, descricao)
        self.tamanho = tamanho
        self.estado = estado

    @property
    def tamanho(self):
        return self.__tamanho
    
    @tamanho.setter
    def tamanho(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Valor invalido")
        self.__tamanho = valor.strip()

    @property
    def estado(self):
        return self.__estado
    
    @estado.setter
    def estado(self, valor: int):
        if not isinstance(valor, int) or not 0 <= valor <= 10: # valor vai de 0/10 a 10/10 
            raise ValueError("Valor invalido, insira um numero de 0 a 10")
        self.__estado = valor

    def exibir_detalhes(self):
        return(f"Item: {self.nome}\n Quantidade: {self.quantidade}\n Tamanho: {self.tamanho}\n Estado:{self.estado}/10\n Descrição: {self.descricao}")
