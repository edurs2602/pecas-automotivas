# Projeto Automotivas

Este projeto é uma aplicação Django que simula um sistema de gerenciamento de peças automotivas e usuários. Ele utiliza um modelo customizado de usuário (com UUID e autenticação via JWT)

## Como Executar com Docker

### Pré-requisitos

- [Docker](https://www.docker.com) instalado.

#### Clone o Repositório

´´´bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_DIRETORIO>
´´´

#### Configure as Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com as seguintes variáveis (ajuste conforme necessário):
´´´bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_NAME=automotivas
POSTGRES_PORT=5432
´´´

#### Suba os Containers
Execute o comando abaixo para construir as imagens e iniciar os containers:
´´´bash
docker-compose up --build
´´´

#### Acesse a Aplicação e os Endpoints da API

- Acesse a aplicação em: [http://localhost:8000](http://localhost:8000/)


