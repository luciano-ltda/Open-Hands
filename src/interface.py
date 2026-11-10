import webbrowser  # Abrir links no navegador
import tkinter as tk  # Interface gráfica (já vem com o Python)
from tkinter import messagebox  # Janelas de aviso
from sistema import Dados

COR = "#ffc24c"  # Cor de fundo de todas as telas
TAMANHO = "1000x650"  # Tamanho da janela (largura x altura)

dados = Dados()  # Todos os métodos de leitura, gravação e validação ficam no sistema.py
usuario_logado = ""  # Guarda quem está logado

janela = None  # Janela principal (criada em iniciar)
imagem = None  # Imagem do título (carregada em iniciar)


def limpar():  # Apaga tudo da janela para desenhar a próxima tela
    for widget in janela.winfo_children():  # Para cada elemento da tela
        widget.destroy()  # Remove
    if imagem:  # Se a imagem foi carregada
        tk.Label(janela, image=imagem).pack(pady=10)  # Coloca a imagem no topo de toda tela


# TELA DE LOGIN
def tela_login():
    limpar()  # Limpa a janela
    tk.Label(janela, text="Faça seu cadastro ou entre com nome de usuário:", font=("Arial", 20, "bold")).pack(pady=10)  # Título
    campo = tk.Entry(janela)  # Campo para digitar
    campo.pack(pady=5)  # Posiciona

    def entrar():  # Roda ao clicar em Entrar
        global usuario_logado  # Vamos alterar a variável global
        nome = campo.get().strip()  # Lê o que foi digitado
        if not dados.usuario_existe(nome):  # Se o usuário não existe
            messagebox.showerror("Erro", "Usuário não encontrado.")  # Avisa
            return  # Para aqui
        usuario_logado = nome  # Guarda o usuário
        tela_inicial()  # Vai para a tela inicial

    tk.Button(janela, text="Entrar", command=entrar).pack(pady=5)  # Botão entrar
    tk.Button(janela, text="Cadastrar", command=tela_cadastro).pack()  # Botão cadastrar


# TELA DE CADASTRO
def tela_cadastro():
    limpar()  # Limpa a janela
    tk.Label(janela, text="Cadastro", font=("Arial", 20, "bold")).pack(pady=10)  # Título
    campos = []  # Lista dos campos de texto
    for texto in ["Nome", "CEP", "Nome de usuário"]:  # Um campo para cada dado
        tk.Label(janela, text=texto + ":").pack()  # Texto
        campo = tk.Entry(janela)  # Campo
        campo.pack(pady=3)  # Posiciona
        campos.append(campo)  # Guarda na lista

    def cadastrar():  # Roda ao clicar em Cadastrar
        global usuario_logado  # Vamos alterar a variável global
        nome, cep, n_usuario = [c.get().strip() for c in campos]  # Lê os três campos
        if not (nome and cep and n_usuario):  # Se algum estiver vazio
            messagebox.showwarning("Atenção", "Preencha todos os campos.")  # Avisa
            return  # Para aqui
        if dados.usuario_existe(n_usuario):  # Se já existe
            messagebox.showerror("Erro", "Esse nome de usuário já existe.")  # Avisa
            return  # Para aqui
        dados.gravar_usuario(n_usuario, nome, cep)  # Grava no usuarios.json
        usuario_logado = n_usuario  # Já fica logado
        tela_inicial()  # Vai para a tela inicial

    tk.Button(janela, text="Cadastrar", command=cadastrar).pack(pady=10)  # Botão cadastrar
    tk.Button(janela, text="Voltar", command=tela_login).pack()  # Botão voltar


# TELA PARA ESCOLHA DE ITEM
def tela_inicial():
    limpar()  # Limpa a janela
    usuario = dados.buscar_usuario(usuario_logado) or {}  # Dados do usuário logado
    nome = usuario.get("nome") or usuario_logado  # Nome completo, ou o usuário se não houver
    tk.Label(janela, text=f"Olá, {nome.split()[0]}!", font=("Arial", 16, "bold")).pack(pady=10)  # Boas-vindas
    tk.Label(janela, text="O que você quer doar?").pack(pady=10)  # Pergunta
    for item in dados.ITENS:  # Um botão para cada item
        tk.Button(janela, text=item, width=20, command=lambda i=item: tela_instituicoes(i)).pack(pady=4)  # Botão
    tk.Button(janela, text="Ver doações", width=20, command=tela_doacoes).pack(pady=(15, 4))  # Mostra as doações do usuário
    tk.Button(janela, text="Sair", command=tela_login).pack(pady=15)  # Volta ao login


# TELA PARA VER DOAÇÕES
def tela_doacoes():
    limpar()  # Limpa a janela
    doacoes = dados.doacoes_de(usuario_logado)  # Doações deste usuário
    tk.Label(janela, text="Minhas doações", font=("Arial", 16, "bold")).pack(pady=10)  # Título
    quadro = tk.Frame(janela, bg=COR)  # Área do botão, presa na parte de baixo
    quadro.pack(side="bottom", pady=10)  # Empacotada antes da lista para sempre aparecer
    lista = tk.Listbox(janela, width=60, height=10)  # Lista de doações
    lista.pack(padx=10, fill="both", expand=True)  # Ocupa o espaço que sobrar
    for d in doacoes:  # Uma linha para cada doação
        lista.insert("end", f"{d['item']} - {d['instituicao']}")  # Item (com detalhes) e instituição
    if not doacoes:  # Se ainda não há doações
        lista.insert("end", "Nenhuma doação registrada ainda.")  # Avisa
    tk.Button(quadro, text="Voltar", command=tela_inicial).pack()  # Botão voltar


# TELA PARA DOAÇÃO
def tela_instituicoes(item):
    limpar()  # Limpa a janela
    instituicoes = dados.ler_json(dados.ARQUIVOS_INSTITUICOES[item])  # Instituições desse item (arquivo inst_*.json)
    tk.Label(janela, text=f"Doar {item}", font=("Arial", 16, "bold")).pack(pady=10)  # Título
    quadro = tk.Frame(janela, bg=COR)  # Área dos botões, presa na parte de baixo da janela
    quadro.pack(side="bottom", pady=10)  # Empacotada antes da lista para sempre aparecer
    lista = tk.Listbox(janela, width=60, height=10)  # Lista de instituições
    lista.pack(padx=10, fill="both", expand=True)  # A lista ocupa só o espaço que sobrar
    for pos, inst in enumerate(instituicoes, start=1):  # Preenche a lista
        lista.insert("end", f"{inst.get('id', pos)} - {inst['nome']}")  # Número e nome
    if not instituicoes:  # Se não há instituições para esse item
        lista.insert("end", "Nenhuma instituição cadastrada para este item.")  # Avisa

    def escolhida():  # Devolve a instituição selecionada
        if not instituicoes or not lista.curselection():  # Se nada foi selecionado
            messagebox.showwarning("Atenção", "Selecione uma instituição.")  # Avisa
            return None  # Sem instituição
        return instituicoes[lista.curselection()[0]]  # Pega pela posição na lista

    def abrir_mapa():  # Abre o link no navegador
        inst = escolhida()  # Pega a instituição
        if inst and inst.get("link"):  # Se escolheu e tem link
            webbrowser.open(inst["link"])  # Abre o link

    def doar():  # Vai para a tela com os dados do item
        inst = escolhida()  # Pega a instituição
        if inst:  # Se escolheu
            tela_item(item, inst)  # Pede nome, quantidade, descrição e os campos específicos

    tk.Button(quadro, text="Abrir mapa", command=abrir_mapa).pack(side="left", padx=5)  # Botão mapa
    tk.Button(quadro, text="Doar", command=doar).pack(side="left", padx=5)  # Botão doar
    tk.Button(quadro, text="Voltar", command=tela_inicial).pack(side="left", padx=5)  # Botão voltar


# TELA COM OS DADOS DO ITEM
def tela_item(item, inst):
    limpar()  # Limpa a janela
    tk.Label(janela, text=f"Dados do item: {item}", font=("Arial", 16, "bold")).pack(pady=10)  # Título
    tk.Label(janela, text=f"Instituição: {inst['nome']}").pack(pady=(0, 10))  # Instituição escolhida
    campos = []  # Campos de texto, na ordem da tela
    extras = [rotulo for _, rotulo, _ in dados.CLASSES_ITEM[item][1]]  # Campos específicos do item
    for texto in ["Nome", "Quantidade", "Descrição"] + extras:  # Campos comuns + específicos
        tk.Label(janela, text=texto + ":").pack()  # Texto
        campo = tk.Entry(janela, width=40)  # Campo
        campo.pack(pady=3)  # Posiciona
        campos.append(campo)  # Guarda na lista

    def confirmar():  # Valida o item e registra a doação
        valores = [c.get().strip() for c in campos]  # Lê todos os campos
        try:
            objeto = dados.criar_item(item, valores)  # O sistema converte e valida
        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))  # Mostra o motivo
            return  # Para aqui
        detalhes = objeto.exibir_detalhes()  # Texto com os detalhes do item
        resumo = f"{item}: " + detalhes.replace("Item: ", "", 1).replace("\n", " | ")  # Tipo e detalhes em uma linha
        dados.doar(usuario_logado, resumo, inst["nome"])  # O sistema grava a doação
        messagebox.showinfo("Obrigado!", f"Você vai doar para: {inst['nome']}\n\n{detalhes}")  # Confirma
        tela_inicial()  # Volta ao início

    tk.Button(janela, text="Confirmar doação", command=confirmar).pack(pady=10)  # Botão confirmar
    tk.Button(janela, text="Voltar", command=lambda: tela_instituicoes(item)).pack()  # Botão voltar


def iniciar() -> None:  # Cria a janela e abre o programa (pode ser chamada por um main.py)
    global janela, imagem  # limpar() e as telas precisam acessar

    janela = tk.Tk()  # Cria a janela
    janela.title("Doação")  # Título
    janela.geometry(TAMANHO)  # Tamanho
    janela.configure(bg=COR)  # Cor de fundo da janela
    janela.option_add("*Label.Background", COR)  # Todos os textos e imagens ficam com o mesmo fundo

    try:  # Tenta carregar a imagem do título
        imagem = tk.PhotoImage(file="titulo.png")  # Abre o arquivo da imagem
        imagem = imagem.zoom(2, 2)  # Aumenta 2 vezes
        imagem = imagem.subsample(3, 3)  # Reduz 3 vezes
    except tk.TclError:  # Se o arquivo não existe ou não abre
        imagem = None  # Segue sem imagem

    tela_login()  # Começa pela tela de login
    janela.mainloop()  # Mantém a janela aberta


if __name__ == "__main__":  # Permite rodar `python interface.py` direto
    iniciar()
