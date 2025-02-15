# Projeto Automotivas

Este projeto é uma aplicação Django que simula um sistema de gerenciamento de peças automotivas e usuários. Ele utiliza um modelo customizado de usuário (com UUID e autenticação via JWT) e integra funcionalidades como upload assíncrono de CSV via Celery.

---

## Como Executar com Docker

### Pré-requisitos

- [Docker](https://www.docker.com) instalado.
- [Docker Compose](https://docs.docker.com/compose/) instalado.

### Clone o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_DIRETORIO>
```

### Configuração do Ambiente

Renomeie o arquivo *.env-example* para *.env* e ajuste os valores conforme necessário.

### Suba os Containers

Execute o comando abaixo para construir as imagens e iniciar os containers:

```bash
docker-compose up --build
```

Os serviços iniciados serão:

- **db**: PostgreSQL.
- **backend**: Aplicação Django (servidor rodando na porta 8000).
- **redis**: Broker para o Celery.
- **celery**: Worker do Celery.

### Acesse a Aplicação e os Endpoints da API

- **Aplicação:** [http://localhost:8000](http://localhost:8000/)
- **Documentação da API com swagger:** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **Documentação da API com redoc:** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## Endpoints Principais e Exemplos de Teste

### Endpoints de Usuários (Users)

- **Registrar Usuário:**  
  ***POST http://localhost:8000/api/users/***  

  **Corpo da Requisição de usuario comum (JSON):**

```json
{
  "username": "novo_usuario",
  "email": "novo_usuario@example.com",
  "user_type": "common",
  "password": "senha123"
}
```
  **Corpo da Requisição de usuario admin (JSON):**

```json
{
  "username": "novo_usuario",
  "email": "novo_usuario@example.com",
  "user_type": "admin",
  "password": "senha123"
}
```

- **Listar/Obter/Atualizar Usuários:**  
  Estes endpoints exigem autenticação via JWT. Por exemplo, para listar usuários:  
  ***GET http://localhost:8000/accounts/api/***  
  Inclua o header:  
```http
Authorization: Bearer SEU_TOKEN_DE_ACESSO
```

### Autenticação via JWT

Para obter um token JWT, envie um POST para o endpoint de autenticação (exemplo: */api/token/*):

```bash
POST http://localhost:8000/api/token/
Content-Type: application/json
```

**Corpo da Requisição:**

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

A resposta será algo como:

```json
{
  "access": "SEU_TOKEN_DE_ACESSO",
  "refresh": "SEU_TOKEN_REFRESH"
}
```

Use o token de acesso para autenticar as demais requisições incluindo o header:

```http
Authorization: Bearer SEU_TOKEN_DE_ACESSO
```

---

### Endpoints de Peças (Parts)

- **Listar Peças:**  
  ***GET http://localhost:8000/parts/api/***  

- **Upload de CSV:**  
  ***POST http://localhost:8000/parts/api/upload_csv/***  

  **Exemplo de Requisição (multipart/form-data):**  
  - **Key:** file  
  - **Value:** (selecione um arquivo CSV com cabeçalhos: *part_number, name, details, price, quantity*)

- **Associar Modelos de Carro a uma Peça:**  
  ***POST http://localhost:8000/parts/api/{id_da_peca}/associate_carmodels/***  

  **Corpo da Requisição (JSON):**

```json
{
  "car_model_ids": [1, 2, 3]
}
```

- **Desassociar Modelo de Carro de uma Peça:**  
  ***POST http://localhost:8000/parts/api/{id_da_peca}/disassociate_carmodel/***  

  **Corpo da Requisição (JSON):**

```json
{
  "car_model_id": 1
}
```

---

### Endpoints de Carros (Cars)

- **Listar Carros:**  
  ***GET http://localhost:8000/cars/api/***  

- **Criar Carro (Apenas Admin):**  
  ***POST http://localhost:8000/cars/api/***  

  **Corpo da Requisição (JSON):**

```json
{
  "name": "Carro Exemplo",
  "manufacturer": "Fabricante X",
  "year": 2021
}
```

- **Obter Peças Associadas a um Carro:**  
  ***GET http://localhost:8000/api/cars/{id_do_carro}/parts/***

---

### Executando os Testes via Docker

Você pode rodar os testes dentro do container do backend com:

```bash
docker-compose run backend pytest
```

Ou, se os containers já estiverem rodando, abra um terminal no container backend:

```bash
docker-compose exec backend bash
```

E, dentro do container, execute:

```bash
pytest
```

Os testes cobrem as principais funcionalidades da aplicação, incluindo as views de upload de CSV, gerenciamento de carros, peças e usuários.

---

## Observações

- **Celery:**  
  Certifique-se de que o worker do Celery está rodando (verifique os logs do container *celery*). O upload de CSV é processado de forma assíncrona.

- **Envio do CSV:**  
  Nesta versão, o conteúdo do CSV é lido e enviado diretamente para a task Celery, evitando problemas de compartilhamento de arquivos entre containers.

- **Persistência de Dados:**  
  O volume do PostgreSQL (*automotivas_db*) é persistido para manter os dados entre reinicializações dos containers.

- **Variáveis de Ambiente:**  
  Renomeie o arquivo *.env-example* para *.env* e ajuste os valores conforme a necessidade do seu ambiente de desenvolvimento ou produção.

Em caso de dúvidas, consulte os logs dos containers com:

```bash
docker-compose logs <service>
```

Siga estas instruções para configurar e testar o projeto com Docker.

