# Q.02 - Na mediana, qual organização possui o top-10 repositórios com mais issues totais?

# Digite, abaixo, a organização que gostaria de pesquisar:
organizacao = "facebook"
# Digite, abaixo, o token de utilização da API do GitHub:
token = ""

print(f"Analisando dados da organização: {organizacao}")

import requests
import statistics

# Verificando a quantidade de páginas:
resposta = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":1}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token}" , "X-GitHub-Api-Version": "2022-11-28"})
if resposta.status_code == 200:
  if "Link" in resposta.headers:
    ultimaUrl = resposta.headers["Link"].split(",")[1]
    indexInicio = resposta.headers["Link"].split(",")[1].find("&page=")
    indexFinal = resposta.headers["Link"].split(",")[1].find(">" , indexInicio)
    totalDePaginas = int(ultimaUrl[indexInicio+6:indexFinal])
    print(f"Quantidade de páginas a serem analisadas: {totalDePaginas}")
  else:
    totalDePaginas = 1
else:
  print("Erro ao acessar API do GitHub")

listaQtdIssuesPorRepositorio = []

pagina = 1
count = 0

while pagina <= totalDePaginas:
  repositorios = requests.get(f"https://api.github.com/orgs/{organizacao}/repos" , params={"per_page": 100 , "page":pagina}, headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token} " , "X-GitHub-Api-Version": "2022-11-28"})
  pagina += 1
  if repositorios.status_code == 200:
    listaRepositorios = repositorios.json()
    for repositorio in listaRepositorios:
      count += 1
      print(count)
      nomeRepositorio = repositorio["name"]
      print(f"\nRecuperando dados do repositório {nomeRepositorio} do {organizacao}")
      qtdIssuesAbertas =  repositorio["open_issues_count"] #requests.get(f"https://api.github.com/search/issues?q=repo:{organizacao}/{nomeRepositorio}+type:issue+state:open" , headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token} " , "X-GitHub-Api-Version": "2022-11-28"})
      print(f"Quantidade de issues abertas: {qtdIssuesAbertas}")
      resposta = requests.get(f"https://api.github.com/search/issues?q=repo:{organizacao}/{nomeRepositorio}+type:issue+state:closed" , headers= {"Accept": "application/vnd.github+json" , "Authorization": f"Bearer {token} " , "X-GitHub-Api-Version": "2022-11-28"})
      if resposta.status_code == 200:
        qtdIssuesFechadas = resposta.json()["total_count"]
        print(f"quantidade de issues fechadas: {qtdIssuesFechadas}")
        listaQtdIssuesPorRepositorio.append(qtdIssuesAbertas + qtdIssuesFechadas)
      else:
        print(f"Erro ao tentar acessar issues fechadas do repositório {nomeRepositorio}.")
        print(f"X-RateLimit-Reset: ")
        print(resposta.headers["X-RateLimit-Reset"])

  print(f"lista com quantidade de issues por repositorio: {listaQtdIssuesPorRepositorio}")
  listaQtdIssuesPorRepositorio.sort(reverse=True)
  print(f"Lista ordenada de quantidade de issues por repositório: {listaQtdIssuesPorRepositorio}")
  print(f"Lista das quantidades de issues para os 10 repositórios com mais issues: {listaQtdIssuesPorRepositorio[:10]}")
  print(f"Mediana dos top-10 repositórios do(a) {organizacao} com mais issues: {statistics.median(listaQtdIssuesPorRepositorio[:10])}")


else:
  print(f"erro ao tentar acessar repositorios da organização. \nStatus da requisição: {repositorios.status_code}")

