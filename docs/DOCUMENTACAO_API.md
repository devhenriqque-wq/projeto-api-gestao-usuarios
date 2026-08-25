# Documentação da API REST Segura para Gestão de Usuários

## 1. Objetivo do projeto

Este projeto implementa uma aplicação web para gerenciamento de usuários. O back-end disponibiliza uma API REST com operações de cadastro, consulta, atualização e exclusão. A autenticação é realizada por meio de JWT e a autorização utiliza controle de acesso baseado em perfis (RBAC).

A aplicação possui três perfis:

- **Administrador:** acesso total ao gerenciamento de usuários.
- **Operador:** pode consultar e atualizar usuários, mas não pode cadastrar, excluir nem alterar perfis.
- **Cliente:** pode visualizar apenas os próprios dados.

---

# Parte 1 – Modelagem da API

A API utiliza recursos representados por URLs, métodos HTTP adequados para cada operação e códigos de resposta compatíveis com os princípios REST.

| Método HTTP | URL | Finalidade | Código de resposta esperado |
|---|---|---|---|
| POST | `/login` | Autenticar usuário e gerar JWT | `200 OK` |
| GET | `/usuarios` | Listar usuários cadastrados | `200 OK` |
| GET | `/usuarios/{id}` | Consultar usuário específico | `200 OK` |
| POST | `/usuarios` | Cadastrar novo usuário | `201 Created` |
| PUT | `/usuarios/{id}` | Atualizar usuário cadastrado | `200 OK` |
| DELETE | `/usuarios/{id}` | Excluir usuário | `204 No Content` |
| GET | `/me` | Consultar os dados do usuário autenticado | `200 OK` |

Também podem ocorrer respostas como:

- `400 Bad Request`: tentativa de operação inválida;
- `401 Unauthorized`: credenciais ou JWT inválidos;
- `403 Forbidden`: usuário autenticado sem permissão;
- `404 Not Found`: usuário não encontrado;
- `409 Conflict`: e-mail já cadastrado.

---

# Parte 2 – Segurança com JWT

## Processo de login

O usuário informa **e-mail** e **senha** na tela de login. O front-end envia os dados ao endpoint `POST /login`.

O back-end consulta o usuário pelo e-mail e compara a senha recebida com o hash armazenado no banco de dados utilizando PBKDF2-HMAC-SHA256.

Se as credenciais estiverem corretas, a API gera um JWT e o devolve ao cliente.

## Geração do token

O token é assinado no servidor utilizando o algoritmo `HS256` e uma chave secreta.

O JWT contém as seguintes informações:

- `sub`: ID do usuário;
- `nome`: nome do usuário;
- `email`: e-mail do usuário;
- `perfil`: perfil de acesso;
- `iat`: data e hora de emissão;
- `exp`: data e hora de expiração.

## Utilização do token

Após o login, o front-end envia o JWT nos endpoints protegidos por meio do cabeçalho HTTP:

```text
Authorization: Bearer <token>
```

A API valida a assinatura e o tempo de validade do token antes de autorizar a operação.

## Política de expiração

Foi adotado o prazo de **60 minutos**.

A escolha busca equilibrar segurança e usabilidade. Um token com duração limitada reduz a janela de utilização caso seja obtido indevidamente. Ao mesmo tempo, 60 minutos é um período suficiente para uma sessão comum de uso da aplicação acadêmica.

---

# Parte 3 – Controle de acesso (RBAC)

A autorização é implementada por meio do perfil armazenado no cadastro do usuário.

## Matriz de permissões

| Operação | Administrador | Operador | Cliente |
|---|:---:|:---:|:---:|
| Fazer login | Sim | Sim | Sim |
| Visualizar os próprios dados | Sim | Sim | Sim |
| Listar usuários | Sim | Sim | Não |
| Consultar outro usuário | Sim | Sim | Não |
| Cadastrar usuário | Sim | Não | Não |
| Atualizar usuário | Sim | Sim | Não |
| Alterar perfil de acesso | Sim | Não | Não |
| Excluir usuário | Sim | Não | Não |

O back-end não confia apenas na interface. Mesmo que um usuário tente chamar diretamente um endpoint pela URL, a API valida seu JWT e seu perfil antes de executar a operação.

Isso impede, por exemplo, que um Cliente chame manualmente `GET /usuarios` ou que um Operador tente executar `DELETE /usuarios/{id}`.

---

# Parte 4 – OAuth 2.0

Embora o OAuth 2.0 não tenha sido implementado, ele poderia ser utilizado para permitir que uma aplicação parceira acessasse recursos da API sem receber a senha do usuário.

## 1. Concessão de acesso

Uma aplicação parceira redirecionaria o usuário para um servidor de autorização. O usuário faria login diretamente nesse ambiente e receberia uma tela informando quais permissões a aplicação está solicitando.

Ao autorizar, a aplicação parceira receberia um código de autorização.

## 2. Utilização de tokens

A aplicação parceira trocaria o código de autorização por um **access token**.

Nas requisições aos recursos protegidos, esse token seria enviado no cabeçalho:

```text
Authorization: Bearer <access_token>
```

A API verificaria o token e permitiria somente os recursos e permissões concedidos.

## 3. Benefícios

O OAuth 2.0 oferece vantagens importantes:

- a aplicação parceira não precisa conhecer a senha do usuário;
- as permissões podem ser delegadas e limitadas;
- o token pode ter validade curta;
- o acesso pode ser revogado;
- é possível utilizar escopos específicos;
- reduz o compartilhamento direto de credenciais.

No contexto deste sistema, um parceiro poderia receber, por exemplo, apenas permissão de consulta de usuários, sem receber permissão para excluir ou alterar cadastros.

---

# Parte 5 – Análise de Segurança

| Risco de segurança | Medida de mitigação adotada |
|---|---|
| Roubo ou reutilização de JWT | Token com expiração de 60 minutos; uso previsto sobre HTTPS em ambiente de produção |
| Senhas armazenadas em texto puro | As senhas são armazenadas somente como hash PBKDF2-HMAC-SHA256 |
| Acesso indevido a endpoints | RBAC validado no back-end em todas as operações protegidas |
| Tentativa de usar token adulterado | Validação da assinatura JWT antes de aceitar o token |
| Acesso com token expirado | O campo `exp` é validado pela biblioteca JWT |
| Cadastro duplicado por e-mail | E-mail definido como único no banco e validação de conflito na API |
| Exposição indevida da chave de assinatura | Chave pode ser definida por variável de ambiente e não deve ser publicada em produção |

## Outras boas práticas aplicadas

- validação de e-mail;
- senha com mínimo de 8 caracteres;
- separação entre autenticação e autorização;
- respostas HTTP adequadas;
- banco de dados não retorna o hash da senha nas respostas;
- validação de permissão feita no servidor;
- cliente não pode visualizar dados de outro cliente;
- operador não pode alterar perfil de acesso;
- administrador autenticado não pode excluir a própria conta pelo endpoint de exclusão.

---

# Web Services e REST

A solução funciona como um Web Service porque disponibiliza recursos e operações por meio do protocolo HTTP.

A abordagem REST foi adotada porque:

- utiliza métodos HTTP padronizados;
- representa usuários como recursos;
- emprega URLs simples;
- utiliza JSON nas requisições e respostas;
- mantém comunicação cliente-servidor;
- permite integração com diferentes aplicações.

---

# Como demonstrar o funcionamento

1. Iniciar o servidor com `uvicorn app.main:app --reload`.
2. Acessar `http://127.0.0.1:8000`.
3. Realizar login com o administrador.
4. Cadastrar um usuário Operador e um Cliente.
5. Demonstrar a listagem, edição e exclusão.
6. Fazer login como Operador e demonstrar que o cadastro e a exclusão não estão disponíveis.
7. Fazer login como Cliente e demonstrar que somente os próprios dados são exibidos.
8. Acessar `http://127.0.0.1:8000/docs` para demonstrar os endpoints da API.

---

# Conclusão

O projeto demonstra uma aplicação web funcional com API REST, CRUD de usuários, autenticação JWT, autorização por RBAC e proteção de endpoints. A solução também apresenta medidas de segurança relacionadas a armazenamento de senhas, expiração de tokens, proteção por perfis e controle de acesso. Além da implementação prática, a documentação contextualiza o uso do OAuth 2.0 em uma possível integração com aplicações parceiras.
