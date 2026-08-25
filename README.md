# API REST Segura para Gestão de Usuários

Projeto acadêmico composto por uma API REST em **Python + FastAPI** e uma interface web simples em **HTML, CSS e JavaScript**.

A solução implementa:

- CRUD de usuários;
- autenticação por e-mail e senha;
- geração e validação de JWT;
- controle de acesso por perfis (RBAC);
- perfis Administrador, Operador e Cliente;
- hash de senhas com PBKDF2-HMAC-SHA256;
- proteção dos endpoints;
- documentação sobre REST, JWT, RBAC, OAuth 2.0 e análise de segurança;
- interface web funcional para demonstrar a API.

## 1. Tecnologias utilizadas

### Back-end
- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- PyJWT
- PBKDF2-HMAC-SHA256

### Front-end
- HTML5
- CSS3
- JavaScript puro

## 2. Como instalar

Abra um terminal dentro da pasta do projeto e execute:

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Como executar

```bash
uvicorn app.main:app --reload
```

Depois acesse:

- Interface web: `http://127.0.0.1:8000`
- Documentação Swagger: `http://127.0.0.1:8000/docs`
- Documentação ReDoc: `http://127.0.0.1:8000/redoc`

## 4. Usuários para demonstração

O projeto entregue inclui um banco de demonstração com:

- Administrador: `admin@demo.com` / `Admin@123`
- Operador: `operador@demo.com` / `Operador@123`
- Cliente: `cliente@demo.com` / `Cliente@123`

Caso o banco seja removido, a aplicação cria automaticamente o Administrador na primeira execução. Os dados do administrador podem ser alterados por variáveis de ambiente conforme o arquivo `.env.example`.

## 5. Perfis de acesso

- **Administrador:** listar, consultar, cadastrar, editar e excluir usuários.
- **Operador:** listar, consultar e editar usuários. Não pode excluir usuários nem alterar perfis.
- **Cliente:** visualiza apenas os próprios dados.

## 6. Como testar

1. Execute o servidor.
2. Abra a interface web.
3. Entre com o usuário administrador.
4. Cadastre usuários com os perfis Operador e Cliente.
5. Faça logout e teste os diferentes níveis de acesso.

Também é possível testar diretamente pela documentação Swagger em `/docs`.

## 7. Estrutura do projeto

```text
projeto_api_gestao_usuarios/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── docs/
│   └── DOCUMENTACAO_API.md
├── evidencias/
│   ├── LEIA-ME_EVIDENCIAS.md
│   ├── RESULTADO_TESTES.txt
│   └── capturas de tela (.png)
├── .env.example
├── README.md
└── requirements.txt
```

## 8. Observação acadêmica

O OAuth 2.0 é explicado na documentação, conforme solicitado na atividade, mas não foi implementado porque o enunciado exige apenas sua contextualização.

## 9. Executando com Docker

### Pré-requisito

Tenha o Docker Desktop instalado e em execução.

### Criar a imagem

Na pasta raiz do projeto, execute:

```bash
docker build -t api-gestao-usuarios .
```

### Executar o container

```bash
docker run -d --name api-gestao-usuarios -p 8000:8000 api-gestao-usuarios
```

### Verificar o container

```bash
docker ps
```

A aplicação ficará disponível em:

- Interface: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Parar e remover o container

```bash
docker stop api-gestao-usuarios
docker rm api-gestao-usuarios
```

### Recriar após alterações

```bash
docker build -t api-gestao-usuarios .
docker run -d --name api-gestao-usuarios -p 8000:8000 api-gestao-usuarios
```
