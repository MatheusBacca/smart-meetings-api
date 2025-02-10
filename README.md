# Gerenciador Inteligente de Reuniões Virtuais (FastAPI + MySQL)

Este projeto é uma API RESTful desenvolvida com [FastAPI](https://fastapi.tiangolo.com/), integrada com o banco de dados [MySQL](https://www.mysql.com/). O sistema permite o CRUD completo de reuniões virtuais!

## Funcionalidades

- **Reservar salas de reunião:** Faça reservas de salas de reunião com informações como:
  - Id da sala;
  - Id do criador;
  - Hora de início da reserva;
  - Hora de conclusão da reserva;
  - Data da criação da reserva;
- **Listar reservas:** Consulte todas as reuniões ou busque por filtros específicos, como:
  - Por id da reseva;
  - Por id da sala;
  - Por id de usuário;
  - Por data de reservas;
  - Por datas de criação;
- **Editar reservas:** Atualize informações de reservas existentes.
- **Excluir reservas:** Cancele reservas através do seu id.

## Tecnologias utilizadas

- **FastAPI:** Framework para desenvolvimento rápido de APIs modernas.
- **MySQL:** Banco de dados relacional e escalável para armazenamento de dados.
- **SQLAlchemy:** ORM para interação otimizada com o banco de dados.
- **Pydantic:** Validação de dados e schemas para requests e responses das APIs.

---

## Pré-requisitos

Certifique-se de ter instalado:

- Python 3.11+;
- MySQL 8+;
- pipenv shell para gerenciamento de dependências;

---

## Instalação e configuração

1. **Clone o repositório:**

   ```powershell
   git clone https://github.com/MatheusBacca/smart-meetings-api.git
   cd smart-meetings-api
2. **Instale as dependências:**

    ```powershell
    pipenv install
3. **Ative o ambiente virtual:**

    ```powershell
    pipenv shell
4. **Crie um banco de dados no MySQL:**
* Guarde do nome escolhido para o banco de dados para ser utilizado mais tarde.

    ```sql
    CREATE DATABASE roomsDatabase;
5. **Atualize o arquivo 'config.cfg' com as credenciais de conexão:**

    ```config.cfg
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=*seu_usuario
    DB_PASSWORD=*sua_senha
    DB_NAME=roomsDatabase
6. **Execute o servidor:**

    ```powershell
    uvicorn main:app --reload
* Você pode consultar a documentação dinâmica e interativa das APIs no link: http://127.0.0.1:8000/docs;
7. **Execute os testes:**

    ```powershell
    pipenv run pytest
---

## Contribuição
* Contribuições são bem-vindas! Siga as etapas abaixo para colaborar:

1. Faça um fork do projeto.
2. Crie uma branch para sua funcionalidade: git checkout -b feature/nova-funcionalidade.
3. Faça suas alterações e commit: git commit -m "Adiciona nova funcionalidade".
4. Envie um pull request.

---

## Licença
Este projeto está licenciado sob a MIT License.
