# Evidências de funcionamento

As evidências desta pasta registram a interface e os testes realizados na aplicação.

| Arquivo | Evidência |
|---|---|
| `01_tela_login.png` | Tela de autenticação por e-mail e senha |
| `02_administrador_listagem.png` | Administrador autenticado com listagem e ações de gestão |
| `03_cadastro_usuario.png` | Formulário de cadastro de usuário |
| `04_perfil_operador.png` | Perfil Operador com acesso intermediário |
| `05_perfil_cliente.png` | Perfil Cliente visualizando somente os próprios dados |
| `06_testes_funcionais_api.png` | Resultado consolidado dos testes funcionais |
| `07_endpoints_api.png` | Endpoints REST implementados |
| `RESULTADO_TESTES.txt` | Registro textual dos testes executados |
| `resultado_testes.json` | Registro estruturado dos testes executados |

## Resultado dos testes

Foram executados 9 testes principais e todos foram aprovados, incluindo login, geração/uso de autenticação, listagem protegida, restrições de RBAC e consulta dos próprios dados pelo Cliente.

## Usuários de demonstração incluídos no banco

- Administrador: `admin@demo.com` / `Admin@123`
- Operador: `operador@demo.com` / `Operador@123`
- Cliente: `cliente@demo.com` / `Cliente@123`
