import requests
import time
import csv

headers = {"Authorization": "token xxxx"}


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
    print('Comecando a mineracao...')
    endCursor = "null"  # Proxima pagina
    nodes = []  # Resultados da query

    # for x in range(interval):
    # GraphQL query
    for x in range(interval):
        query = """
            {
                search(query: "stars:>100 language:Python", type: REPOSITORY, first: %s, after:%s) {
                  pageInfo {
                    endCursor
                  }
                  nodes {
                    ... on Repository {
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
              """ % (first, endCursor)

        # O resultado da query que contem a proxima pagina e os nodes
        queryResult = run_query(query)
        queryResultData = queryResult['data']['search']['nodes']
        querySize = len(queryResultData)
        for y in range(querySize):
            # Salva os nodes no array de nodes
            if queryResultData[y]['primaryLanguage'] != None and queryResultData[y]['primaryLanguage']['name'] == 'Python':
                nodes.append(queryResultData[y])
            # Pega o endCursor aka proxima pagina
            endCursor = '"{}"'.format(
                queryResult["data"]["search"]["pageInfo"]["endCursor"])

        if x == interval/2:
            print('Metade minerada, aguente firme!')
        else:
            print(str(x) + ': 100 minerados!!!')
    return nodes

# Escreve em um arquivo csv


def writeCsv(nodes):
    print('Comecando a escrever o arquivo csv!')

    with open("/Users/Rafael/Desktop/labex2/SPRINT_II/csv_files/mil_repos.csv", 'w') as new_file:

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


nodes = mine(100, 10)
writeCsv(nodes)
