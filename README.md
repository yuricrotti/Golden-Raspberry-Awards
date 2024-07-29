# Golden Raspberry Awards

## Visão Geral

Este projeto foi projetado para gerenciar e analisar dados de premiações de filmes no Golden Raspberry Awards. A aplicação utiliza um banco de dados SQLite para armazenar informações sobre os filmes e suas premiações, e inclui funcionalidades para processamento de dados e testes.

O SQLite foi escolhido por ser um banco de dados leve e fácil de configurar, adequado para o escopo deste projeto (uso em memória).

## Estrutura do Diretório

* `data/`: Contém o arquivo `movielist.csv`, que inclui a lista de filmes e seus detalhes.
* `database/`: Contém o arquivo `database.py`, responsável por inicializar e gerenciar o banco de dados.
* `models/`: Contém o arquivo `models.py`, que define os modelos do banco de dados.
* `repositories/`: Contém o arquivo `repositories.py`, que lida com operações do banco de dados.
* `schemas/`: Contém o arquivo `schemas.py`, que define os esquemas de dados.
* `tests/`: Contém arquivos de teste para o projeto.

obs: Esse projeto está configurado para rodar na porta 8000, verique se você não tem nenhum outro serviço rodando nela. 
## Instalação

1. Clone o repositório:
   ```sh
   git clone https://github.com/yuricrotti/Golden-Raspberry-Awards.git
   cd Golden-Raspberry-Awards
   ```

2. Crie um ambiente virtual:
   ```sh
   python -m venv .venv
   ```

3. Ative o ambiente virtual:

    No Windows:
    ```sh
    .venv\Scripts\activate
    ```
    
    No macOS/Linux:
    ```sh
    source .venv/bin/activate
    ```

4. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Testes

Para rodar os testes, utilize o comando:
```sh
make test
```

# Teste de Integração (github actions)

Este projeto utiliza GitHub Actions para realizar testes de integração contínua. O workflow de integração contínua é definido no arquivo .github/workflows/python-ci.yml.
Este workflow configura um ambiente de integração contínua que verifica automaticamente o código sempre que há novas alterações (push ou pull requests) na main. 
.

# Documentação da API
Para visualizar a documentação interativa da API, acesse http://localhost:8000/docs. 
Esta documentação é gerada automaticamente pelo Swagger e é embutida no FastAPI, proporcionando uma interface amigável para explorar e testar os endpoints da API.

## Docker

Este projeto usa Docker para facilitar a construção, execução e implantação da aplicação. Siga as instruções abaixo para construir e executar o contêiner Docker.

### Pré-requisitos

- Certifique-se de ter o Docker instalado na sua máquina. Você pode baixar e instalar o Docker a partir do [site oficial](https://www.docker.com/get-started).

### Construindo a Imagem Docker

Para construir a imagem Docker, use o seguinte comando:

```sh
docker build . -t app-awards
```

Executando o Contêiner Docker
```sh
docker run -p 8000:8000 app-awards
```
