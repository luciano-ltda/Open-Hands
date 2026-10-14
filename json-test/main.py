import json

ARQ = "dados.json"

def carregar():
	try:
		with open(ARQ, "r", encoding="utf-8") as file:
			if file == "":
				return []
			return json.load(file)
	except FileNotFoundError:
		print("Arquivo não encontrado\n")
		return []
	except json.JSONDecodeError:
		print("Erro de decodificação\n")
		return []

def salvar(dados):
	try:
		with open(ARQ, "w", encoding="utf-8") as file:
			json.dump(dados, file, ensure_ascii=True, indent=2)
			print("Dados Salvos")
	except FileNotFoundError:
		print("Arquivo não encontrado\n")
		return []
	except json.JSONDecodeError:
		print("Erro de decodificação\n")
		return []

def adicionar(item):
	dados = carregar()
	dados.append(item)
	salvar(dados)

def clean():
	print("Arquivo Limpo")
	salvar([])

def ler():
	try:
		with open(ARQ, "r", encoding="utf-8") as file:
			print(*file, sep='\n')
	except FileNotFoundError:
		print("Arquivo não encontrado\n")
		return []
	except json.JSONDecodeError:
		print("Erro de decodificação\n")
		return []

def main():
	while True:
		frase = input("Entrada de dados > ")
		if frase == "clean":
			clean()
			continue
		elif frase == "end":
			break
		elif frase == "ler":
			ler()
			break
		adicionar(frase)

main()