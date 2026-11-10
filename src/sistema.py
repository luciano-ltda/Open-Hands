from item_alimento import ItemAlimento
from item_brinquedo import ItemBrinquedo
from item_higiene import ItemHigiene
from item_racao import ItemRacao
from item_roupa import ItemRoupa

class Dados:
    ITENS = ["Alimento", "Brinquedo", "Higiene", "Ração", "Roupa"] # Lista de tipos de itens

    ARQUIVOS_INSTITUICOES = {
        "Alimento": "inst_alimento.json",
        "Brinquedo": "inst_brinquedo.json",
        "Higiene": "inst_higiene.json",
        "Ração": "inst_racao.json",
        "Roupa": "inst_roupa.json",
    }

    CLASSES_ITEM = {
        "Alimento": (ItemAlimento, [("validade", "Validade (DD/MM/AAAA)", False)]),
        "Brinquedo": (ItemBrinquedo, [("estado", "Estado de conservação (0 a 10)", True)]),
        "Higiene": (ItemHigiene, [("validade", "Validade (DD/MM/AAAA)", False)]),
        "Ração": (ItemRacao, [("validade", "Validade (DD/MM/AAAA)", False)]),
        "Roupa": (ItemRoupa, [("tamanho", "Tamanho (ex.: P, M, G, 42)", False),
                              ("estado", "Estado de conservação (0 a 10)", True)]),
    }

    def __init__(self, pasta="data"): # Construtor com nome de arquivos permanentes
        self.pasta = Path(pasta) # Pasta padrão (data/)
        self.pasta.mkdir(parents=True, exist_ok=True) # Cria a pasta de dados se não existir
        self.arquivo_usuarios     = self.pasta / "usuarios.json"
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

    def achar_arquivo(self, arquivo) -> Path:
        pastas = [Path("."), self.pasta]
        for pasta in pastas:
            if (pasta / arquivo).exists():
                return pasta / arquivo
        for pasta in pastas:
            if pasta.is_dir():
                for outro in pasta.iterdir():
                    if outro.name.lower() == arquivo.lower():
                        return outro
        return Path(arquivo)

    def ler_json(self, arquivo) -> list:
        caminho = self.achar_arquivo(arquivo)
        try:
            if not caminho.exists():
                return []
            texto = caminho.read_text(encoding="utf-8")
            return json.loads(texto) if texto.strip() else []
        except json.JSONDecodeError:
            print(f"Aviso: {caminho} corrompido\n")
            return []

    def criar_item(self, tipo, valores):
        classe, campos = self.CLASSES_ITEM[tipo]
        nome, quantidade, descricao, *extras = valores
        try:
            quantidade = int(quantidade)
        except ValueError:
            raise ValueError("A quantidade deve ser um número inteiro.") from None
        convertidos = []
        for (chave, _, numerico), valor in zip(campos, extras):
            if numerico:
                try:
                    valor = int(valor)
                except ValueError:
                    raise ValueError(f"O campo {chave} deve ser um número inteiro.") from None
            convertidos.append(valor)
        return classe(nome, quantidade, descricao, *convertidos)
