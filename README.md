# Golden Raspberry Awards

## Visão Geral

Este projeto foi projetado para gerenciar e analisar dados de premiações de filmes no Golden Raspberry Awards. A aplicação utiliza um banco de dados SQLite para armazenar informações sobre os filmes e suas premiações, e inclui funcionalidades para processamento de dados e testes.

O SQLite foi escolhido por ser um banco de dados leve e fácil de configurar, adequado para o escopo deste projeto.

## Estrutura do Diretório

* `data/`: Contém o arquivo `movielist.csv`, que inclui a lista de filmes e seus detalhes.
* `database/`: Contém o arquivo `database.py`, responsável por inicializar e gerenciar o banco de dados.
* `models/`: Contém o arquivo `models.py`, que define os modelos do banco de dados.
* `repositories/`: Contém o arquivo `repositories.py`, que lida com operações do banco de dados.
* `schemas/`: Contém o arquivo `schemas.py`, que define os esquemas de dados.
* `tests/`: Contém arquivos de teste para o projeto.

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
pytest tests/ . 
```
