import requests
import time
import csv

headers = {"Authorization": "token 6207e9b60742649092a01fc229a44ee4746a3672"}


def run_query(query):
    request = requests.post('https://api.github.com/graphql',
                            json={'query': query}, headers=headers)
    while (request.status_code == 502):
        time.sleep(2)
        request = requests.post(
            'https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))

# Minera os repositórios


def mine(first, interval):
    endCursor = "null"  # Proxima pagina
    nodes = []  # Resultados da query

    # for x in range(interval):
    # GraphQL query

    query = """
          {
            user(login: "gvanrossum") {
              repositories(first: 23) {
                nodes {
                  nameWithOwner
                  url
                  stargazers {
                    totalCount
                  }
                  watchers {
                    totalCount
                  }
                  forks {
                    totalCount
                  }
                  releases {
                    totalCount
                  }
                  createdAt
                  primaryLanguage {
                    name
                  }
                }
              }
            }
          }
          """

    # O resultado da query que contem a proxima pagina e os nodes
    queryResult = run_query(query)
    querySize = len(queryResult['data']['user']['repositories']['nodes'])
    for y in range(querySize):
        # Salva os nodes no array de nodes
        nodes.append(queryResult['data']['user']['repositories']['nodes'][y])
        # Pega o endCursor aka proxima pagina
        # endCursor = '"{}"'.format(
        #     queryResult["data"]["search"]["pageInfo"]["endCursor"])

    return nodes

# Escreve em um arquivo csv


def writeCsv(nodes):
    with open("/Users/Rafael/Desktop/labex2/repos.csv", 'w') as new_file:

        fnames = [
            'name_with_owner',
            'url',
            'stars',
            'watchers',
            'forks',
            'releases',
            'created_at',
            'primary_language'
        ]

        csv_writer = csv.DictWriter(new_file, fieldnames=fnames)
        csv_writer.writeheader()
        for node in nodes:
            csv_writer.writerow(
                {
                    'name_with_owner': node['nameWithOwner'],
                    'url': node['url'],
                    'stars': node['stargazers']['totalCount'],
                    'watchers': node['watchers']['totalCount'],
                    'forks': node['forks']['totalCount'],
                    'releases': node['releases']['totalCount'],
                    'created_at': node['createdAt'],
                    'primary_language': node['primaryLanguage']['name'] if node['primaryLanguage'] != None else 'null',
                })

        print('Arquivo csv gerado com sucesso!')


nodes = mine(0, 1)
writeCsv(nodes)
