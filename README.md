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
- testes automatizados com Pytest;
- integração contínua com GitHub Actions;
- construção automatizada da imagem Docker no fluxo de CI/CD;
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

### Testes e automação

- Pytest
- FastAPI TestClient
- HTTPX
- GitHub Actions
- Docker

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
- Health check: `http://127.0.0.1:8000/health`

## 4. Usuários para demonstração

O banco de dados local não é versionado no repositório por segurança.

Na primeira execução, a aplicação cria automaticamente o banco de dados e o usuário Administrador inicial.

Credenciais padrão para demonstração:

- Administrador: `admin@demo.com` / `Admin@123`

Os dados do Administrador podem ser configurados por variáveis de ambiente conforme o arquivo `.env.example`.

Os usuários com perfis Operador e Cliente podem ser cadastrados pelo Administrador durante a demonstração da aplicação.

## 5. Perfis de acesso

- **Administrador:** listar, consultar, cadastrar, editar e excluir usuários.
- **Operador:** listar, consultar e editar usuários. Não pode excluir usuários nem alterar perfis.
- **Cliente:** visualiza apenas os próprios dados.

## 6. Como testar

### Teste manual

1. Execute o servidor.
2. Abra a interface web.
3. Entre com o usuário administrador.
4. Cadastre usuários com os perfis Operador e Cliente.
5. Faça logout e teste os diferentes níveis de acesso.

Também é possível testar diretamente pela documentação Swagger em `/docs`.

### Testes automatizados

O projeto possui testes automatizados utilizando **Pytest** e **FastAPI TestClient**.

Os testes estão localizados em:

```text
tests/test_api.py
```

Atualmente são executados 6 testes automatizados:

- Health check da API;
- rota principal;
- login sem credenciais;
- proteção da listagem de usuários sem autenticação;
- proteção do endpoint de perfil sem autenticação;
- proteção da consulta de usuário sem autenticação.

Para executar os testes localmente, instale as dependências necessárias:

```bash
pip install pytest httpx
```

Depois execute:

```bash
python -m pytest -v
```

O resultado esperado é:

```text
6 passed
```

## 7. CI/CD com GitHub Actions

O projeto utiliza **GitHub Actions** para automatizar a validação da aplicação.

O workflow está localizado em:

```text
.github/workflows/main.yml
```

O processo de CI/CD é executado em eventos de `push` e `pull_request` direcionados à branch `main`.

### CI - Continuous Integration

A etapa de CI realiza:

1. download do código do repositório;
2. configuração do Python;
3. instalação das dependências;
4. instalação das dependências utilizadas pelos testes;
5. validação da importação da API;
6. execução automática dos testes unitários com Pytest.

Comando utilizado para os testes:

```bash
python -m pytest -v
```

A integração só é considerada aprovada quando todos os testes são executados com sucesso.

### CD - Continuous Delivery

Após a aprovação da etapa de CI, o workflow executa a etapa de CD.

Nessa etapa é realizada a construção da imagem Docker da aplicação:

```bash
docker build -t gestao-usuarios .
```

A etapa de CD depende da conclusão bem-sucedida da etapa de CI.

Dessa forma, uma falha nos testes impede a continuidade do fluxo automatizado.

## 8. Estrutura do projeto

```text
projeto-api-gestao-usuarios/
├── .github/
│   └── workflows/
│       └── main.yml
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── docs/
│   └── DOCUMENTACAO_API.md
│
├── evidencias/
│   ├── LEIA-ME_EVIDENCIAS.md
│   ├── RESULTADO_TESTES.txt
│   └── capturas de tela (.png)
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── tests/
│   └── test_api.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── CHECKLIST_ENTREGA.txt
├── Dockerfile
├── EXECUTAR_LINUX_MAC.sh
├── EXECUTAR_WINDOWS.bat
├── GUIA_SEMANA_4_DOCKER.txt
├── README.md
└── requirements.txt
```

## 9. Observação acadêmica

O OAuth 2.0 é explicado na documentação, conforme solicitado na atividade, mas não foi implementado porque o enunciado exige apenas sua contextualização.

## 10. Executando com Docker

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

## 11. Segurança

O projeto aplica mecanismos básicos de segurança para uma API REST:

- autenticação por e-mail e senha;
- senhas armazenadas utilizando PBKDF2-HMAC-SHA256;
- salt aleatório para proteção das senhas;
- autenticação baseada em JWT;
- expiração dos tokens;
- autorização baseada em perfis (RBAC);
- proteção dos endpoints;
- banco de dados local não versionado;
- arquivo `.env` ignorado pelo Git;
- configuração de variáveis de ambiente por meio do `.env.example`.

## 12. Evidências

A pasta `evidencias/` contém capturas de tela e resultados utilizados para demonstrar o funcionamento da aplicação.

Entre as evidências estão:

- tela de login;
- listagem pelo Administrador;
- cadastro de usuário;
- perfil Operador;
- perfil Cliente;
- testes funcionais da API;
- endpoints da API.

Além dessas evidências, o histórico do GitHub demonstra a utilização de:

- Pull Requests;
- GitHub Actions;
- CI;
- CD;
- testes automatizados;
- execução dos testes antes do merge;
- construção da imagem Docker.

## 13. Resultado dos testes automatizados

Os testes automatizados foram integrados ao workflow do GitHub Actions.

Na execução validada após a integração dos testes à branch `main`, foram executados:

```text
test_health PASSED
test_rota_principal PASSED
test_login_sem_credenciais PASSED
test_listar_usuarios_sem_token PASSED
test_consultar_perfil_sem_token PASSED
test_usuario_inexistente_sem_token PASSED

6 passed
```

Isso demonstra que os endpoints básicos e os mecanismos de proteção testados estão funcionando conforme esperado.
