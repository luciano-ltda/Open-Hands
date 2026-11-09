from .sistema import Dados # importa a classe de gerenciamento de dados

class Usuario:  
    def __init__(self, nome, cep, n_usuario):  # Construtor
        self.nome = nome  # Guarda o nome da pessoa
        self.cep = cep  # Guarda o CEP
        self.n_usuario = n_usuario  # Guarda o nome de usuário para o login

    def registro(self, db: Dados) -> None:  # Método que grava o nome de usuário no arquivo
        db.gravar_usuario(self.n_usuario, self.nome, self.cep )

