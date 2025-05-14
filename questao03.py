# RQ 03. Na mediana, qual organização possui o top-10 repositórios com mais contribuições via PR?

import requests
import statistics

#Adicione abaixo o seu token do github
token = ""
#Adicione abaixo o nome da organizacao que deseja pesquisar repositorios
organizacao = "microsoft"

print(f"Verificando dados sobre a organização {organizacao}")

# Verificando a quantidade de páginas:
resposta = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":1}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
if(resposta.status_code == 200):
  ultimaUrl = resposta.headers["Link"].split(",")[1]
  indexInicio = resposta.headers["Link"].split(",")[1].find("&page=")
  indexFinal = resposta.headers["Link"].split(",")[1].find(">" , indexInicio)
  totalDePaginas = int(ultimaUrl[indexInicio+6:indexFinal])
  print(f"Quantidade de páginas de repositórios a serem analisadas: {totalDePaginas}")
else:
  print("Erro ao acessar API do GitHub")

contribuicoesNoRepositorio = []
pagina = 1

while pagina <= totalDePaginas:
  repositorios = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":pagina}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
  pagina += 1
  if repositorios.status_code == 200:
    listaRepositorios = repositorios.json()
    for repositorio in listaRepositorios:
      contribuicoes = 0
      nomeRepositorio = repositorio["name"]
      print(f"\nRecuperando dados do repositório {nomeRepositorio} do {organizacao}")

      # Verificando a quantidade de páginas de detalhamento de pulls:
      resposta = requests.get(f"https://api.github.com/repos/{organizacao}/{nomeRepositorio}/pulls?state=closed" , params={"per_page": 100 , "page":1}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
      if(resposta.status_code == 200):
        if "Link" in resposta.headers:
          ultimaUrl = resposta.headers["Link"].split(",")[1]
          indexInicio = resposta.headers["Link"].split(",")[1].find("&page=")
          indexFinal = resposta.headers["Link"].split(",")[1].find(">" , indexInicio)
          totalDePaginas2 = int(ultimaUrl[indexInicio+6:indexFinal])
          print(f"Quantidade de páginas de pulls a serem analisadas: {totalDePaginas2}")
        else:
          totalDePaginas2 = 1
      else:
        print("Erro ao acessar API do GitHub")
      paginaDePulls = 1
      while paginaDePulls <= totalDePaginas2:
        print(f"Consumindo dados da página {paginaDePulls} de pulls")
        paginaDePulls += 1
        pullsFechados = requests.get(f"https://api.github.com/repos/{organizacao}/{nomeRepositorio}/pulls?state=closed" , params={"per_page": 100 , "page":paginaDePulls}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
        if pullsFechados.status_code == 200:
          pullsFechados = pullsFechados.json()
          for pullFechado in pullsFechados:
            if pullFechado["merged_at"] is not None:
              contribuicoes+=1
        else:
          print(f"Erro ao tentar acessar pulls fechados do repositório {nomeRepositorio}. \nStatus Code: . \nDetalhamento do erro: ")
      contribuicoesNoRepositorio.append(contribuicoes)
      print(f"Total de contribuições do repositório {nomeRepositorio}:  {contribuicoes}")
      print(f"Lista de contribuições em repositórios: {contribuicoesNoRepositorio}")
  else:
    print(f"erro ao tentar acessar repositorios da organização. \nStatus da requisição: {repositorios.status_code}")

print(f"\nLista decrescente de quantidade de contribuições por repositório da organização {organizacao}:")
contribuicoesNoRepositorio.sort(reverse=True)
print(contribuicoesNoRepositorio)
print(f"\nMediana das 10 maiores quantidades de contribuições nos repositórios da organização {organizacao}:")
print(statistics.median(contribuicoesNoRepositorio[:10]))

