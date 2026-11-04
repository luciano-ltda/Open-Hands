from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nome, cep, email, telefone):
        self.nome = nome
        self.cep = cep
        self.email = email
        self.telefone = telefone

    @abstractmethod
    def tipo(self):
        pass
