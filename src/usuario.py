import json  # Importa o módulo para ler e gravar arquivos JSON
import os  # Importa o módulo para verificar se um arquivo existe

class Usuario:  
    def __init__(self, nome, cep, n_usuario):  # Construtor
        self.nome = nome  # Guarda o nome da pessoa
        self.cep = cep  # Guarda o CEP
        self.n_usuario = n_usuario  # Guarda o nome de usuário para o login

    def registro(self):  # Método que grava o nome de usuário no arquivo
        arquivo = "usuario.json"  # Nome do arquivo onde os dados ficam guardados

        if os.path.exists(arquivo):  # Verifica se o arquivo já existe
            with open(arquivo, "r", encoding="utf-8") as f:  # Lê o arquivo
                dados = json.load(f)  # Converte o JSON do arquivo em uma lista Python
        else:  # Se o arquivo ainda não existe
            dados = []  # Começa com uma lista vazia

        dados.append(self.n_usuario)  # Adiciona o nome de usuário no final da lista

        with open(arquivo, "w", encoding="utf-8") as f:  # Abre em modo escrita ("w"), regravando tudo
            json.dump(dados, f)  # Converte a lista em JSON e grava no arquivo
