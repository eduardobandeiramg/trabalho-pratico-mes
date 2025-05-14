# RQ 04 - Na mediana, qual organização possui o top-10 repositórios que lança releases com mais frequência?
# Métrica: total de releases

import requests
import statistics

# Digite abaixo o nome da organização que gostaria de pesquisar:
organizacao = "google"
# Digite abaixo o valor do token do github:
token = ""

print(f"Analisando dados da organização: {organizacao}")

# Verificando a quantidade de páginas:
resposta = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":1}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
if resposta.status_code == 200:
  if "Link" in resposta.headers:
    ultimaUrl = resposta.headers["Link"].split(",")[1]
    indexInicio = resposta.headers["Link"].split(",")[1].find("&page=")
    indexFinal = resposta.headers["Link"].split(",")[1].find(">" , indexInicio)
    totalDePaginas = int(ultimaUrl[indexInicio+6:indexFinal])
    print(f"\nQuantidade de páginas a serem analisadas: {totalDePaginas}")
  else:
    totalDePaginas = 1
else:
  print("Erro ao tentar consumir API do GitHub!")

listaDeQuantidadesDeReleases = []
pagina = 1

while pagina <= totalDePaginas:
  print(f"\nColetando dados da página {pagina}")
  requisicaoRepos = requests.get(f"https://api.github.com/orgs/{organizacao}/repos", params={"per_page": 100 , "page":pagina} , headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
  pagina += 1
  if requisicaoRepos.status_code == 200:
    listaDeRepositorios = requisicaoRepos.json()
    for repositorio in listaDeRepositorios:
      numeroDeReleases = 0
      nomeDoRepositorio = repositorio["name"]
      print(f"\nBuscando informações sobre o repositório {nomeDoRepositorio}")
      # Verificando a quantidade de páginas de releases:
      resposta = requests.get(f"https://api.github.com/repos/{organizacao}/{nomeDoRepositorio}/releases" , params={"per_page": 100 , "page":1}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
      if resposta.status_code == 200:
        if "Link" in resposta.headers:
          ultimaUrl = resposta.headers["Link"].split(",")[1]
          indexInicio = resposta.headers["Link"].split(",")[1].find("&page=")
          indexFinal = resposta.headers["Link"].split(",")[1].find(">" , indexInicio)
          totalDePaginas2 = int(ultimaUrl[indexInicio+6:indexFinal])
        else:
          totalDePaginas2 = 1
        if(totalDePaginas2 == 1):
          numeroDeReleases = len(resposta.json())
        else:
          paginasAdicionais = requests.get(f"https://api.github.com/repos/{organizacao}/{nomeDoRepositorio}/releases" , params={"per_page": 100 , "page":totalDePaginas2}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
          paginasAdicionais = paginasAdicionais.json()
          paginasAdicionais = len(paginasAdicionais)
          numeroDeReleases = ((totalDePaginas2 - 1) * 100) + paginasAdicionais
      else:
        print(f"Erro ao acessar dados de releses do repositorio {nomeDoRepositorio}")
      print(f"Número de releases: {numeroDeReleases}")
      print(f"Pagina {pagina}/{totalDePaginas}")
      listaDeQuantidadesDeReleases.append(numeroDeReleases)
  else:
    print(f"Erro ao buscar releases do repositório {nomeDoRepositorio} da organização {organizacao}")

listaDeQuantidadesDeReleases.sort(reverse=True)
print(f"Lista decrescente da quantidade de releases para cada repositório da organização {organizacao}")
print(listaDeQuantidadesDeReleases)
print(f"Mediana da quantidade de releases dos top-10 repositórios com maior frequência de releases: ")
print(statistics.median(listaDeQuantidadesDeReleases[:10]))
