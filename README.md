[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![SO](https://img.shields.io/badge/Platform-Linux-bringhtgreen)
![Ubuntu](https://img.shields.io/badge/Ubuntu-20.04-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.10-blue)
[![Versão do Docker](https://img.shields.io/badge/Docker-%3E%3D17.06-blue.svg)](https://www.docker.com/)
![API Badge](https://img.shields.io/badge/API-healthcare_finance_api-brightgreen)


<h1> geospatial-api </h1>
<br>

Este repositório contém a implementação de uma API REST que contempla o back-end de uma aplicação para submissão de dados geoespaciais e permite a busca de um endereço ou localização a partir da API do FreeGeoCoding.


## Sumário

1. [Instalação](#instalation)
   - [Instalação em modo de desenvolvedor](#instalation_dev_mode)
   - [Instalação em modo de produção](#instalation_prod_mode)
2. [Utilização](#usage)
   - [Endpoint geometry](#endpoint_geometry)
        - [Inserção de geometria](#endpoint_geometry_post)
        - [Consulta de geometria pelo id](#endpoint_geometry_get_id)
        - [Consulta de geometria pelo description](#endpoint_geometry_get_description)
        - [Atualização da geometria](#endpoint_geometry_put)
        - [Remoção da geometria](#endpoint_geometry_delete)
   - [Endpoint address](#endpoint_address)
        - [Consulta de endereços pelo nome de uma localização](#endpoint_placename_address)
        - [Consulta de endereços pelo endereço de uma localização](#endpoint_get_address)
   - [Endpoint coordinates](#endpoint_coordinates)
        - [Consulta de uma localização utilzando a API do FreeGeoCoding](#endpoint_coordinates)
3. [Testes](#tests)
   - [Testar as funcionalidades de geometry](#test_geometry)
   - [Testar as funcionalidades de free_geocoding](#test_free_geocoding)


<a id="instalation"></a>
## Instalação

A implementação do geospatial-api depende essencialmente de:

- [Flask](https://flask.palletsprojects.com/en/latest/)
- [Flask-smorest](https://flask-smorest.readthedocs.io/en/latest/)
- [Flask-sqlalchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)


Para começar a utilizar a API e ter acesso ao código-fonte do software, siga os passos abaixo para clonar o repositório:

### **1.** Clone o repositório de software:

Utilize o seguinte comando para clonar o repositório para o seu ambiente local:

    git clone https://github.com/YuriDomaradzki/geospatial_api.git

### **2.** Acesse a Pasta do Código-Fonte:

Navegue até a pasta do código-fonte do projeto utilizando o comando `cd`. Certifique-se de estar no diretório correto antes de prosseguir.

    cd geospatial_api

<a id="instalation_dev_mode"></a>
## Instalação em modo desenvolvedor - GitHub 

Para realizar a instalação em modo de desenvolvedor do projeto a partir do GitHub, siga os passos abaixo:

### **1.** Instalação no Modo de Desenvolvimento:

Utilize o comando `make install` para realizar a instalação em modo de desenvolvimento. Este comando irá configurar o ambiente, instalar dependências e preparar o projeto para ser executado localmente.

    make install

### **2.** Execução em Modo de Desenvolvimento:

Utilize o comando `make run` no diretório raiz do projeto para executá-lo em modo de desenvolvimento, resultando na criação de um servidor em modo de desenvolvimento:

    make run

<br>

<a id="instalation_prod_mode"></a>
## Instalação em modo de produção - GitHub 

Para realizar a instalação em modo de desenvolvedor utiizando docker containers siga os passos abaixo:

### **1.** Instale o Docker caso ainda não esteja instalado (tutorial de [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)):

    make install_docker

### **2.** Instalação e Execução no Modo de Desenvolvimento:
Utilize o comando `make build` para realizar a instalação e execução da aplicação em modo de produção. Este comando irá criar uma imagem docker do projeto e subir um container a partir dela. Porém, é necessário editar o arquivo docker-compose.yml antes com as credenciais desejadas para o banco de dados (está configurada com os valores padrões):

    make build

<a id="usage"></a>
## Utilização

A seção de utilização disponibiliza definições e exemplos para cada ponto de extremidade da API geospatial-api. Para facilitar o uso da API, pode-se utilizar o <a href="https://insomnia.rest/download">Insomnia</a>.


<a id="endpoint_geometry"></a>
### **1.** Endpoint: geometry
O endpoint `geometry` é projetado para fornecer informações detalhadas sobre as geometrias armazenadas no sistema. Ele oferece uma maneira eficiente e segura de acessar dados relevantes sobre as geometrias registradas. Utilizando este endpoint, os desenvolvedores podem obter informações cruciais, como ID da geometria, descrição e coordenadas geoespaciais.

**Recursos Principais:**
- Inserir geometria
- Recuperar geometria por id
- Recuperar geometria por descrição
- Atualizar geometria
- Deletar geometria

<a id="endpoint_geometry_post"></a>
#### **6.1.** Inserir geometria [POST]

**Endpoint:**

    POST http://127.0.0.1:5000/geometry

**Headers:**

    {
        'Content-Type': 'application/json',
        'X-Custom-Header': json.dumps(
            {
                {
                    "geom": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [30.0, 10.0],
                                [40.0, 40.0],
                                [20.0, 40.0],
                                [10.0, 20.0],
                                [30.0, 10.0]
                            ]
                        ]
                    },
                    "description": "My First Polygon"
                }
            }
        )
    }

**Retorno:**

    {
        "Success": "Geometry added!"
    }

<a id="endpoint_geometry_get_id"></a>
#### **6.2.** Buscar geometria por id [GET]

**Endpoint:**

    GET http://127.0.0.1:5000/geometry?id=1

**Retorno:**

    [
        {
            "DESCRIPTION": "My First Polygon",
            "GEOMETRY": "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
            "ID": 1
        }
    ]

<a id="endpoint_geometry_get_description"></a>
#### **6.3.** Consulta de geometria pela descrição [GET]

**Endpoint:**

    GET http://127.0.0.1:5000/geometry

**Headers:**

    {
        'Content-Type': 'application/json',
        'X-Custom-Header': json.dumps(
            {
                "description": "My First Polygon"
            }
        )
    }

**Retorno:**

    [
        {
            "DESCRIPTION": "My First Polygon",
            "GEOMETRY": "POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))",
            "ID": 1
        }
    ]

<a id="endpoint_geometry_put"></a>
#### **6.4.** Atualizar geometria pelo id [PUT]

**Endpoint:**

    PUT http://127.0.0.1:5000/geometry?id=1

**Headers:**

    {
        'Content-Type': 'application/json',
        'X-Custom-Header': json.dumps(
            {
                {
                    "geom": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [20.0, 10.0],
                                [40.0, 40.0],
                                [20.0, 40.0],
                                [10.0, 20.0],
                                [20.0, 10.0]
                            ]
                        ]
                    },
                    "description": "My Updated Polygon"
                }
            }
        )
    }

**Retorno:**

    {
        "Success": "The geometry was updated successfully"
    }

<a id="endpoint_geometry_delete"></a>
#### **6.4.** Remoção da geometria pelo id [DELETE]

**Endpoint:**

    DELETE http://127.0.0.1:5000/geometry?id=1

**Retorno:**

    {
        "Sucess": "The geometry with id 1 was deleted with successfully"
    }


<a id="endpoint_address"></a>
### **7.** Endpoint: Adress
O endpoint `address` é dedicado a fornecer informações detalhadas sobre endereços, utilizando a integração com APIs de dados geoespaciais de terceiros, como a API do FreeGeoCoding. Este endpoint oferece uma abordagem eficiente e segura para acessar dados relevantes relacionados à localização. Ao utilizar este endpoint, os desenvolvedores podem obter informações cruciais, como identificador do endereço, localização e detalhes específicos relacionados aos serviços de geocodificação.

**Recursos Principais:**
- Consulta de endereços pelo nome de uma localização
- Consulta de endereços pelo endereço de uma localização

<a id="endpoint_placename_address"></a>
#### **7.1.** Consulta de endereços pelo nome de uma localização [GET]

**Endpoint:**

    GET http://127.0.0.1:5000/adresses?placename=<placename>

**payload:**

    {
        "api_key": "<api_key>"
    }

**Exemplo:**

    GET http://127.0.0.1:5000/adresses?placename=Statue+of+Liberty

**Retorno:**

    {
	    "adresses": [
            {
                "boundingbox": [
                    "40.6888049",
                    "40.6896741",
                    "-74.0451069",
                    "-74.0439637"
                ],
                "class": "tourism",
                "display_name": "Statue of Liberty, Flagpole Plaza, Manhattan Community Board 1, Manhattan, New York County, New York, 10004, United States",
                "importance": 0.8714324085707771,
                "lat": "40.689253199999996",
                "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                "lon": "-74.04454817144321",
                "osm_id": 32965412,
                "osm_type": "way",
                "place_id": 317737799,
                "type": "attraction"
            }, ...
        ]
    }


<a id="endpoint_get_address"></a>
#### **7.2.** Consulta de endereços pelo endereço de uma localização [GET]

**Endpoint:**

    GET http://127.0.0.1:5000/adresses?street=<street>>&city=<city>&state=<state>&postalcode=<postalcode>&country=<country>

**payload:**

    {
        "api_key": "<api_key>"
    }

**Exemplo:**

    GET http://127.0.0.1:5000/adresses?street=Praça Roberto Gomes Pedrosa&city=São Paulo&state=SP&postalcode=05653-070&country=BR

**Retorno:**

    {
        "adresses": [
            {
                "boundingbox": [
                    "-23.5983031",
                    "-23.5982885",
                    "-46.7200457",
                    "-46.7198977"
                ],
                "class": "highway",
                "display_name": "Praça Roberto Gomes Pedrosa, Morumbi, São Paulo, Região Imediata de São Paulo, Região Metropolitana de São Paulo, Região Geográfica Intermediária de São Paulo, São Paulo, Southeast Region, 05653-070, Brazil",
                "importance": 1.00001,
                "lat": "-23.5983031",
                "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
                "lon": "-46.719971",
                "osm_id": 934412829,
                "osm_type": "way",
                "place_id": 8049364,
                "type": "primary"
            }, ...
        ]
    }


<a id="endpoint_coordinates"></a>
### **8.** Endpoint: coordinates
O endpoint `coordinates` é dedicado a fornecer informações detalhadas a partir de um par de coordenadas geográficas. Utilizando a integração com APIs de dados geoespaciais de terceiros, como a API do FreeGeoCoding, este endpoint oferece uma abordagem eficiente e segura para acessar dados relevantes relacionados à localização. Ao utilizar este endpoint, os desenvolvedores podem obter informações cruciais, como identificador do endereço, e detalhes específicos relacionados aos serviços de geocodificação, baseados nas coordenadas fornecidas.

**Recursos Principais:**
- Consulta de endereços pela coordenada

<a id="endpoint_coordinates"></a>
#### **8.1.** Consulta de endereços pela coordenada [GET]

**Endpoint:**

    GET http://127.0.0.1:5000/coordinates?lat=<lat>&lon=<lon>

**payload:**

    {
        "api_key": "<api_key>"
    }

**Exemplo:**

    GET http://127.0.0.1:5000/coordinates?lat=40.7558017&lon=-73.9787414

**Retorno:**

    {
        "coordinates": {
            "address": {
                "ISO3166-2-lvl4": "US-NY",
                "city": "New York",
                "country": "United States",
                "country_code": "us",
                "county": "New York County",
                "house_number": "555",
                "neighbourhood": "Midtown East",
                "postcode": "10017",
                "road": "5th Avenue",
                "state": "New York",
                "suburb": "Manhattan"
            },
            "boundingbox": [
                "40.7557517",
                "40.7558517",
                "-73.9787914",
                "-73.9786914"
            ],
            "display_name": "555, 5th Avenue, Midtown East, Manhattan, New York County, New York, 10017, United States",
            "lat": "40.7558017",
            "licence": "Data © OpenStreetMap contributors, ODbL 1.0. https://osm.org/copyright",
            "lon": "-73.9787414",
            "osm_id": 2716012085,
            "osm_type": "node",
            "place_id": 319634907
        }
    }


<a id="tests"></a>
## Testes

Nesta seção, você encontrará os testes relacionados às funcionalidades da API.


<a id="test_patients"></a>
### **1.** Testar as funcionalidades de geometry

A seguir, estão alguns cenários de teste para validar as funcionalidades relacionadas as geometrias:

 - Validação da criação de uma nova geometria com dados válidos (test_post_valid_geometry);
 - Verificação do retorno adequado quando nenhuma informação de campo é fornecida (test_post_none_field_information);
 - Checagem da resposta para dados inválidos fornecidos na postagem (test_post_invalid_field_information);
 - Consulta de Geometria;
 - Verificação da obtenção de informações corretas com um ID válido (test_geometry_with_valid_id);
 - Validação da resposta ao consultar com um ID em branco (test_geometry_with_blank_id);
 - Verificação da resposta para um ID inválido (test_geometry_with_invalid_id);
 - Checagem da resposta ao consultar com um ID inexistente (test_geometry_with_nonexistent_id);
 - Atualização de Geometria;
 - Verificação da atualização bem-sucedida com um ID válido (test_put_valid_geometry);
 - Checagem da resposta para tentativa de atualização com um ID inválido (test_put_invalid_geometry);
 - Exclusão de Geometria;
 - Validação da exclusão bem-sucedida com um ID válido (test_delete_valid_geometry);
 - Verificação da resposta para tentativa de exclusão com um ID inválido (test_delete_invalid_geometry);

 Utilize o comando `make test_patient` para executar os casos de teste:

    make test_patient

<a id="test_pharmacies"></a>
### **2.** Testar as funcionalidades de Pharmacies

A seguir, estão alguns cenários de teste para validar as funcionalidades relacionadas às farmácies:

 - Listagem de Farmácias para garantir a obtenção de uma lista válida ao estar autenticado.
 - Obtenção de Farmácia por Nome Válido para verificar a obtenção de informações corretas com um nome válido e rejeição de nomes inválidos ao estar autenticado.
 - Obtenção de Farmácia por Nome Inválido para validar a impossibilidade de obter informações de farmácias com nome inválido, mesmo estando autenticado.
 - Obtenção de Farmácia por Cidade Válida para assegurar a obtenção de informações corretas por uma cidade válida ao estar autenticado.
 - Obtenção de Farmácia por Cidade Inválida para verificar a impossibilidade de obter informações de farmácias com cidade inválida, mesmo estando autenticado.
 - Obtenção de Farmácia por Nome e Cidade Válidos para garantir a obtenção de informações corretas com nome e cidade válidos ao estar autenticado.
 - Obtenção de Farmácia por Cidade Inválida e Nome Válido para validar a impossibilidade de obter informações de farmácias com cidade inválida, mesmo com nome válido, estando autenticado.
 - Obtenção de Farmácia por Cidade Válida e Nome Inválido para validar a impossibilidade de obter informações de farmácias com nome inválido, mesmo com cidade válida, estando autenticado.

 Utilize o comando `make test_pharmacy` para executar os casos de teste:

    make test_pharmacy


<a id="test_transactions"></a>
### **3.** Testar as funcionalidades de Transactions

A seguir, estão alguns cenários de teste para validar as funcionalidades relacionadas as transações:

 - Listagem de Transações para garantir a obtenção de uma lista válida ao estar autenticado.
 - Obtenção de Transações por Nome de Farmácia Válido para verificar a obtenção de informações corretas com um nome de farmácia válido e rejeição de nomes inválidos ao estar autenticado.
 - Obtenção de Transações por Nome de Farmácia Inválido para validar a impossibilidade de obter informações de transações com nome de farmácia inválido, mesmo estando autenticado.
 - Obtenção de Transações por Nome de Farmácia e Data de Transação Válidos para garantir a obtenção de informações corretas com nome de farmácia e data válidos ao estar autenticado.
 - Obtenção de Transações por Nome de Farmácia Inválido e Data de Transação Válida para validar a impossibilidade de obter informações de transações com nome de farmácia inválido, mesmo com data válida, estando autenticado.

 Utilize o comando `make test_transactions` para executar os casos de teste:

    make test_transactions

<a id="test_user"></a>
### **4.** Testar as funcionalidades de User

A seguir, estão alguns cenários de teste para validar as funcionalidades relacionados aos usuários:

 - Obtenção de Informações do Usuário com Nome de Usuário Válido: Garante que seja possível obter informações do usuário com um nome de usuário válido ao estar autenticado.
 - Obtenção de Informações do Usuário com Nome de Usuário Inválido: Garante que não seja possível obter informações do usuário com um nome de usuário inválido ao estar autenticado.
 - Logout: Verifica se o processo de logout ocorre corretamente, encerrando a sessão do usuário autenticado.
 - Login com Nome de Usuário Válido e Senha Inválida: Valida que não seja possível realizar o login com um nome de usuário válido e senha inválida.
 - Login com Nome de Usuário Inválido e Senha Válida: Valida que não seja possível realizar o login com um nome de usuário inválido e senha válida.

 Utilize o comando `make test_user` para executar os casos de teste:

    make test_user

<a id="code_patterns"></a>
## Garantir Padrões e estilo de códigos de forma automatizada

A utilização do comando `make lint` é uma prática fundamental para garantir a padronização e o estilo do código de maneira automatizada. Este comando incorpora diversas ferramentas e processos que analisam o código-fonte, assegurando sua conformidade com as diretrizes estabelecidas. Para utilizá-lo, entre no diretório raiz do projeto e execute o seguinte comando:

    make lint
