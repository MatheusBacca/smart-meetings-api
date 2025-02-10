# Gerenciador Inteligente de Reuniões Virtuais (FastAPI + MySQL)

Este projeto é uma API RESTful desenvolvida com [FastAPI](https://fastapi.tiangolo.com/), integrada com o banco de dados [MySQL](https://www.mysql.com/). O sistema permite o CRUD completo de reuniões virtuais!

## Algumas funcionalidades

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
- **Excluir reservas:** Cancele reservas através do seu id.

## Tecnologias utilizadas

- **FastAPI:** Framework para desenvolvimento rápido de APIs modernas.
- **MySQL:** Banco de dados relacional e escalável para armazenamento de dados.
- **SQLAlchemy:** ORM para interação otimizada com o banco de dados.
- **Pydantic:** Validação de dados e schemas para requests e responses das APIs.
- **Pytest:** Testes unitários das APIs do servidor.

---

## Pré-requisitos

Certifique-se de ter instalado:

- Python 3.12+;
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

## Exemplos de uso
1. Crie um usuário para utilização no servidor;
   * POST /users
    ```json
   {"name": "seu_nome", "password": "sua_senha", "email": "seu_email"}
2. Autentique-se na API: POST /rooms;
    ```json
   {"username": "seu_nome", "password": "sua_senha"}
3. Crie uma nova sala;
   * POST /rooms
    ```json
   {"name": "nome_da_sala", "location": "localizacao_da_sala", "capacity": 5}
4. Verifique a disponibilidade desta sala em um período desejado;
   * GET /rooms/1/availability
5. Se tiver disponível no período desejado, autentique-se na API: POST /reservations;
    ```json
   {"username": "seu_nome", "password": "sua_senha"}
6. Crie uma reserva para esta sala;
   * POST /reservations
    ```json
   {"room_id": 1, "start_time": "2025-02-10T15:00:00", "end_time": "2025-02-10T16:00:00"}
7. Liste todas os registros criados:
   1. GET /users?id=1;
   2. GET /rooms?id=1;
   3. GET /reservations?room_id=1 ou GET /rooms/1/reservations;
8. Se desejar cancelar esta reserva:
   * DELETE /reservations/1;
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
