import json
import os
from pathlib import Path

class Dados:
    ITENS = ["Alimento", "Brinquedo", "Higiene", "Ração"] # Lista de tipos de itens

    def __init__(self, pasta="data"): # Construtor com nome de arquivos permanentes
        self.pasta = Path(pasta) # Pasta padrão (data/)
        self.pasta.mkdir(parents=True, exist_ok=True) # Cria a pasta de dados se não existir
        self.arquivo_usuarios     = self.pasta / "usuarios.json"
        self.arquivo_instituicoes = self.pasta / "instituicoes.json"
        self.arquivo_historico    = self.pasta / "historico.json"

    def _ler(self, caminho, padrao) -> list: # Leitura com verificação de erro
        try:
            if not caminho.exists() or caminho.stat().st_size == 0: # se não existir ou arquivo vazio, retorna lista vazia
                print("Arquivo não encontrado\n")
                return padrao
            with caminho.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Aviso: {caminho} corrompido\n")
            return padrao

    def _gravar(self, caminho, dados) -> None: # Escreve os dados em seu arquivo correto
        caminho.parent.mkdir(parents=True, exist_ok=True) # Cria a pasta se não existir
        tmp = caminho.with_suffix(caminho.suffix + ".tmp") # Cria arquivos temporários para dump de dados
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2) # formatação do JSON
            f.flush()            # VVV
            os.fsync(f.fileno()) # sincronização de dados com a memória
        os.replace(tmp, caminho) # concretiza o arquivo temporario

    def ler_usuarios(self) -> dict: # usa a função genérica para ler o arquivo de usuários, retorna uma lista de pares
        return self._ler(self.arquivo_usuarios, {})

    def usuario_existe(self, username) -> bool: # verifica se um usuario existe no banco de dados
        return username in self.ler_usuarios()

    def buscar_usuario(self, username) -> dict | None: # procura o nome de um usuario
        return self.ler_usuarios().get(username)

    def gravar_usuario(self, username, nome, cep) -> None: # registra o nome de um usuario na base de dados
        usuarios = self.ler_usuarios()
        usuarios[username] = {"nome": nome, "cep": cep}
        self._gravar(self.arquivo_usuarios, usuarios)

    def ler_instituicoes(self) -> dict: # Leitura dos nomes das instituições, com a verificação de erro de _ler()
        padrao = {tipo: [] for tipo in self.ITENS} # dict comprehension para gerar valor de fallback
        dados = self._ler(self.arquivo_instituicoes, padrao) # leitura genérica
        for tipo in self.ITENS: # Verificação caso dados não coincidam da lista ITENS com a base de dados
            if tipo not in dados:
                dados[tipo] = []
        return dados

    def instituicoes_por_tipo(self, tipo) -> list: # retorna a lista de instituições por tipo
        return self.ler_instituicoes().get(tipo, [])

    def ler_historico(self) -> dict: # lê o histórico de doações geral
        return self._ler(self.arquivo_historico, {})

    def doacoes_de(self, username) -> list: # lê o histórico de doações específico
        return self.ler_historico().get(username, [])

    def doar(self, username, item, instituicao) -> None: # registra uma doação no histórico
        historico = self.ler_historico()
        if username not in historico: # se não estiver no histórico, cria a instância e adiciona
            historico[username] = []
        historico[username].append({"item": item, "instituicao": instituicao})
        self._gravar(self.arquivo_historico, historico)