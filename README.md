# 🍕 FastAPI - Delivery de Pizzaria

Estou criando uma API REST para gerenciamento de pedidos, clientes e produtos de uma pizzaria.  
Construída com **FastAPI**, **SQLAlchemy** e autenticação com **JWT**.

---

## 🚀 Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno e rápido
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI para rodar a aplicação
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para manipulação do banco de dados
- [Alembic](https://alembic.sqlalchemy.org/) - Migrations do banco
- [Passlib](https://passlib.readthedocs.io/en/stable/) - Hash de senhas com Bcrypt
- [Python-Jose](https://python-jose.readthedocs.io/en/latest/) - Geração/validação de tokens JWT
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Carregar variáveis de ambiente
- [python-multipart](https://andrew-d.github.io/python-multipart/) - Suporte a uploads de arquivos

---

## 🧱 Funcionalidades

- Cadastro e login de usuários com autenticação JWT
- Cadastro de produtos (pizzas, bebidas, etc)
- Gerenciamento de pedidos
- Upload de imagens para o cardápio (usando `multipart/form-data`)
- Registro de clientes e endereços de entrega
- Relacionamento entre clientes, pedidos e itens

---

## 📁 Estrutura de Pastas

```bash
pizzaria/
├── app/
│ ├── main.py # Inicialização do FastAPI
│ ├── models/ # Modelos SQLAlchemy
│ ├── schemas/ # Pydantic (entrada e saída de dados)
│ ├── routes/ # Endpoints da API
│ ├── services/ # Lógicas e regras de negócio
│ ├── auth/ # Geração e verificação de tokens JWT
│ ├── database.py # Conexão e criação do banco
│ └── config.py # Carregamento de variáveis .env
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Como executar

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/pizzaria-fastapi.git
cd pizzaria-fastapi
```

2. **Crie e ative um ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure o .env**

Crie um arquivo .env com:

5. **Execute a aplicação**

```bash
uvicorn app.main:app --reload
```

6. **Acesse a documentação**

- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

---

### 📌 Contribuição
Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades.
Para isso, abra um PR ou issue com sua sugestão.

---

### 🧑‍💻 Autor

Desenvolvido por Ariel França
- 🔗 [Meu linkedIn](https://www.linkedin.com/in/arielvinis/)
- 📧 [ariel.franca@hotmail.com](ariel.franca@hotmail.com)
