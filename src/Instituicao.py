from usuario import Usuario

class Instituicao(Usuario):
    def __init__(self, nome, cep, email, telefone):
        super().__init__(nome, cep, email, telefone)

    def tipo(self):
        return "Instituição"
