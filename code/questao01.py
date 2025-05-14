# Q.01 - Na mediana, qual organização possui o top-10 repositórios mais antigos?

# Digite, abaixo, a organização que gostaria de pesquisar:
organizacao = "google"
# Digite, abaixo, o token de utilização da API do GitHub:
token = ""

print(f"Analisando dados da organização: {organizacao}")

import requests
from datetime import datetime

# Verificando a quantidade de páginas:
resposta = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":1}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
ultimaUrl = resposta.headers["Link"].split(",")[1]
indexInicio = resposta.headers["Link"].split(",")[1].find("&page=")
indexFinal = resposta.headers["Link"].split(",")[1].find(">" , indexInicio)
totalDePaginas = int(ultimaUrl[indexInicio+6:indexFinal])
print(f"Quantidade de páginas a serem analisadas: {totalDePaginas}")

listaRepositorios = []
listaDatasCriacao = []
pagina = 1

while pagina <= totalDePaginas:
  print(f"Consumindo dados da página {pagina}")
  repos = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":pagina}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
  if repos.status_code == 200:
    listaRepos = repos.json()
    for repo in listaRepos:
      listaDatasCriacao.append(repo["created_at"])
  else:
    print(f"Erro ao acessar end-point. \nStatus: {repos.status_code} \nMensagem: {repos.json()}")
  pagina += 1

listaDatasCriacao.sort()
print(f"tamanho da lista: {len(listaDatasCriacao)}")
print(listaDatasCriacao[:10])
ano = int(listaDatasCriacao[5][:4])
mes = int(listaDatasCriacao[5][5:7])
dia = int(listaDatasCriacao[5][8:10])
dataMaisRecente = datetime(ano , mes , dia)
ano = int(listaDatasCriacao[4][:4])
mes = int(listaDatasCriacao[4][5:7])
dia = int(listaDatasCriacao[4][8:10])
dataMaisAntiga = datetime(ano , mes , dia)
mediaDiferencaEntreDatas = (dataMaisRecente - dataMaisAntiga)/2
print(f"Mediana dos TOP-10 repositórios mais antigos da organização {organizacao}: {dataMaisAntiga + mediaDiferencaEntreDatas}")

