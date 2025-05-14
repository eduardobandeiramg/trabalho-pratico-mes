# RQ 05. Na mediana, qual organização possui o top-10 repositórios atualizado com mais frequência?

# Digite, abaixo, o nome da organização que gostaria de pesquisar:
organizacao = "google"
# Digite, abaixo, o token de acesso à API do GitHub:
token = ""

print(f"\nAvaliando métricas da organização: {organizacao}")

from datetime import datetime
import requests
import statistics


# Verificando a quantidade de páginas:
resposta = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":1}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
if "Link" in resposta.headers:
  ultimaUrl = resposta.headers["Link"].split(",")[1]
  indexInicio = resposta.headers["Link"].split(",")[1].find("&page=")
  indexFinal = resposta.headers["Link"].split(",")[1].find(">" , indexInicio)
  totalDePaginas = int(ultimaUrl[indexInicio+6:indexFinal])
  print(f"\nQuantidade de páginas a serem analisadas: {totalDePaginas}")
else:
  totalDePaginas = 1

temposAteUltimaAtualizacao = []
hoje = datetime.now()
pagina = 1

while pagina <= totalDePaginas:
  repositorios = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":pagina}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
  pagina +=1
  if(repositorios.status_code == 200):
    repositorios = repositorios.json()
    count = 0
    for repo in repositorios:
      nomeDoRepositorio = repo["name"]
      print(f"\nColetando dados do repositório {nomeDoRepositorio}")
      commits = requests.get(f"https://api.github.com/repos/{organizacao}/{nomeDoRepositorio}/commits" , headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
      if(commits.status_code == 200):
        dataUltimoCommit = commits.json()[0]["commit"]["author"]["date"]
        dataUltimoCommit = datetime.strptime(dataUltimoCommit, "%Y-%m-%dT%H:%M:%SZ")
        tempoAteUltimaAtualizacao = hoje - dataUltimoCommit
        print(f"tempo em relação à última atualização: {tempoAteUltimaAtualizacao}")
        temposAteUltimaAtualizacao.append(tempoAteUltimaAtualizacao)
      else:
        print(f"Erro ao buscar commits do repositório {nomeDoRepositorio}")

  else:
    print("Erro ao buscar repositórios")
    print(f"Código do retorno: {repositorios.status_code}")
    print(f"Mensagem de retorno: {repositorios.json()}")

temposAteUltimaAtualizacao.sort()
temposAteUltimaAtualizacao = temposAteUltimaAtualizacao[:10]
print("Lista ordenada dos tempos até ultima atualização:")
print(temposAteUltimaAtualizacao)
print("Mediana do tempo entre atualizações dos 10 repositórios atualizados mais recentemente:")
print(statistics.median(temposAteUltimaAtualizacao))