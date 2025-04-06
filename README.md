# Projeto FastAPI de Cálculo de Prêmios de Seguro

## Pré-requisitos

Antes de começar, certifique-se de ter as seguintes ferramentas instaladas em sua máquina:

* **Python 3.13+:** Necessário para executar o projeto localmente.
* **pip:** Gerenciador de pacotes do Python (geralmente incluído com a instalação do Python).
* **Docker:** Necessário para executar o projeto utilizando Docker. Você pode instalá-lo em [https://www.docker.com/get-started/](https://www.docker.com/get-started/).

## Execução Local (com Ambiente Virtual)

Estas instruções guiam você na configuração e execução do projeto em um ambiente virtual isolado.

1.  **Clone o Repositório**


2.  **Crie um Ambiente Virtual:**
    ```bash
    python -m venv venv
    ```

3.  **Ative o Ambiente Virtual:**
    * **No Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **No Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    
5.  **Execute a Aplicação:**
    Navegue até o diretório onde o seu arquivo principal do FastAPI (geralmente chamado `main.py` ou similar) está localizado e execute o seguinte comando:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    
6.  **Acesse a Aplicação:**
    A aplicação estará disponível em seu navegador ou ferramenta de teste de API (como Postman ou Insomnia) no endereço `http://127.0.0.1:8000`. Você pode acessar a documentação interativa da API em `http://127.0.0.1:8000/docs` ou a documentação OpenAPI em formato JSON em `http://127.0.0.1:8000/openapi.json`.

7.  **Desativar o Ambiente Virtual (opcional):**
    Quando terminar de trabalhar no projeto, você pode desativar o ambiente virtual com o comando:
    ```bash
    deactivate
    ```

## Execução com Docker

Estas instruções mostram como construir e executar o projeto utilizando Docker.

1.  **Construa a Imagem Docker:**
    Navegue até a raiz do seu projeto (onde o `Dockerfile` e `docker-compose.yml` estão localizados) e execute o seguinte comando:
    * **Usando `docker build`:**
        ```bash
        docker build -t car-insurance .
        ```

4.  **Execute o Container Docker:**
    * **Usando `docker run`:**
        ```bash
        docker run -p 8000:8000 car-insurance
        ```
       

5.  **Acesse a Aplicação:**
    A aplicação estará disponível em seu navegador ou ferramenta de teste de API no endereço `http://localhost:8000`. A documentação da API estará em `http://localhost:8000/docs`.

