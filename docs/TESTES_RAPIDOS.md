# Testes rápidos da API

Com a aplicação em execução, o fluxo recomendado é:

1. Fazer login com `admin@demo.com` e `Admin@123`.
2. Copiar o `access_token` retornado.
3. Usar o token no cabeçalho `Authorization: Bearer <token>`.
4. Criar um usuário Operador.
5. Criar um usuário Cliente.
6. Listar os usuários.
7. Atualizar um usuário.
8. Excluir um usuário que não seja o administrador autenticado.
9. Entrar como Operador e verificar que cadastro, exclusão e alteração de perfil são bloqueados.
10. Entrar como Cliente e verificar que apenas os próprios dados podem ser consultados.

A documentação interativa do FastAPI em `/docs` permite executar todos esses testes diretamente pelo navegador.
