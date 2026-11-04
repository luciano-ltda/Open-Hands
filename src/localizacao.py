from doador import Doador
from instituicao import Instituicao
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class Localizacao:
    def __init__(self):
        self.geo = Nominatim(user_agent="openhands")

    def coordenadas(self, cep):
        dados = requests.get(f"https://viacep.com.br/ws/{cep}/json/").json()
        if "erro" in dados:
            return None
        endereco = f"{dados['logradouro']}, {dados['localidade']}, {dados['uf']}, Brasil"
        local = self.geo.geocode(endereco) or self.geo.geocode(f"{dados['localidade']}, {dados['uf']}, Brasil")
        if local is None:
            return None
        return (local.latitude, local.longitude)

    def calcular_distancia(self, doador, instituicao):
        a = self.coordenadas(doador.cep)
        b = self.coordenadas(instituicao.cep)
        if a is None or b is None:
            return None
        return geodesic(a, b).km
