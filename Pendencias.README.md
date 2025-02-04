# Pendências/Updates para Fazer

## 1. Na Rota de Delete
- O usuário deve estar logado. Quando o usuário clicar no botão "Delete Account" no frontend, será aberto um formulário onde será solicitado o e-mail e senha para autenticação.
- Após validar, será enviado um código gerado aleatoriamente para o e-mail da conta do usuário.
- Para deletar a conta, o usuário deve fornecer o código gerado no formulário de confirmação.

## 2. Implementar Autenticação com:
- GitHub
- LinkedIn
- Google

## 3. Corrigir o Tempo de Exclusão do Token

## 4. Desempenho e Escalabilidade
- **Cache**: Implemente caching para reduzir a carga no banco de dados e melhorar o desempenho. Você pode usar Redis ou Memcached para armazenar resultados de consultas frequentes.
- **Paginação**: Para endpoints que retornam listas grandes, implemente a paginação para melhorar o desempenho e a usabilidade.
- **Limitação de Taxa**: Implemente limitação de taxa (rate limiting) para proteger sua API contra abusos e garantir que todos os usuários tenham acesso justo aos recursos.

## 5. Autenticação Multi-Fator (MFA)

**Descrição**: Implementar uma camada extra de segurança utilizando autenticação multi-fator. O usuário deve fornecer um código adicional gerado por um aplicativo de autenticação (por exemplo, Google Authenticator).

**Tarefas**:
- Integrar com um serviço de autenticação (ex: Google Authenticator).
- Adicionar uma rota para enviar o código MFA ao usuário.
- Verificar o código MFA ao autenticar.

**Status**: Pendente

## 6. Sistema de Reset de Senha

**Descrição**: Implementar a funcionalidade de redefinição de senha para usuários que esqueceram suas credenciais.

**Tarefas**:
- Criar uma rota para solicitação de redefinição de senha.
- Enviar um link de redefinição de senha por e-mail.
- Implementar uma verificação de segurança para a validade do link.
- Permitir a redefinição da senha.

**Status**: Pendente

## 7. Expiração do Token de Acesso e Renovação

**Descrição**: Melhorar a expiração e renovação do token de acesso. Adicionar uma rota para renovar o token usando um refresh token.

**Tarefas**:
- Implementar refresh tokens que possam ser usados para obter novos tokens de acesso sem reautenticar.
- Criar uma rota para a renovação do token.

**Status**: Pendente

## 8. Suporte a Permissões Baseadas em Funções (RBAC)

**Descrição**: Implementar um controle de acesso mais granular baseado em papéis (roles) e permissões específicas.

**Tarefas**:
- Definir diferentes papéis e permissões no sistema (ex: "admin", "user", "moderator").
- Configurar endpoints para verificar se o usuário tem permissão para executar uma ação específica (verificar permissão por ação).
- Melhorar o middleware de verificação de permissões.

**Status**: Pendente

## 9. Melhorias na Validação de Dados de Entrada

**Descrição**: Melhorar a validação dos dados de entrada nas rotas de criação e atualização de usuários.

**Tarefas**:
- Validar que o e-mail fornecido pelo usuário seja único na criação e atualização.
- Garantir que a senha atenda aos critérios de segurança (comprimento mínimo, caracteres especiais, etc.).

**Status**: Pendente

## 10. Testes Automatizados

**Descrição**: Criar testes automatizados para garantir que as rotas de autenticação, autorização e CRUD de usuários funcionem corretamente.

**Tarefas**:
- Escrever testes para rotas de login e CRUD de usuários.
- Testar cenários com usuários sem autenticação, com tokens expirados e com papéis inválidos.

**Status**: Pendente

## 11. Documentação da API com OpenAPI

**Descrição**: Melhorar a documentação da API utilizando o Swagger UI integrado ao FastAPI.

**Tarefas**:
- Adicionar descrições mais detalhadas para todas as rotas.
- Utilizar os exemplos de entrada e saída nas rotas da documentação.
- Adicionar autenticação no Swagger para permitir o uso de tokens.

**Status**: Pendente

## 12. Logs de Segurança e Auditoria

**Descrição**: Implementar logging para rastrear tentativas de login, falhas de autenticação e outras operações críticas.

**Tarefas**:
- Adicionar logs de falhas de login e tentativas de acesso a endpoints restritos.
- Criar um sistema de auditoria para monitorar alterações nos dados de usuários.

**Status**: Pendente

## 13. Mecanismo de Bloqueio de Conta (Rate Limiting e Brute Force Protection)

**Descrição**: Implementar proteção contra ataques de força bruta e limitar o número de tentativas de login.

**Tarefas**:
- Implementar limites de tentativas de login com bloqueio temporário após várias falhas.
- Adicionar verificação de CAPTCHA para impedir bots.

**Status**: Pendente

## 14. Aprimorar Segurança de Armazenamento de Senhas

**Descrição**: Garantir que as senhas dos usuários sejam armazenadas de forma segura e que o algoritmo de hash utilizado esteja atualizado.

**Tarefas**:
- Atualizar o algoritmo de hash das senhas para um mais seguro, como Argon2 ou bcrypt.
- Implementar um mecanismo de atualização de senha (migrar senhas antigas para um hash mais seguro).

**Status**: Pendente
