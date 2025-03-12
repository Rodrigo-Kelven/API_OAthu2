## Autenticação com OAuth2: Guia Completo e Exemplo de Implementação com FastAPI
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
![FastAPI](https://img.shields.io/badge/FastAPI-%23FF4F00.svg?style=for-the-badge&logo=fastapi&logoColor=white)
## Versão 0.10.5
### Este projeto implementa uma aplicação com autenticação de usuários utilizando o protocolo OAuth2, um padrão amplamente utilizado para autenticação e autorização em APIs e sistemas web. A seguir, discutiremos em detalhes o que é o OAuth2, como ele funciona, e como este projeto simplifica seu uso com o framework FastAPI.

## O que é OAuth2?

#### OAuth2 (Open Authorization 2.0) é um protocolo de autorização que permite que você conceda acesso a recursos protegidos sem precisar compartilhar suas credenciais com terceiros. Em vez de fornecer sua senha diretamente a um serviço ou aplicação, você usa um token de acesso temporário, que é emitido após uma autenticação bem-sucedida.
## Como funciona o OAuth2?

#### O OAuth2 é composto por fluxos (ou "flows") de autenticação que permitem que as aplicações solicitem permissões para acessar recursos protegidos em nome do usuário. O fluxo básico de autenticação com OAuth2 geralmente segue esses passos:

- O usuário se autentica: O usuário fornece suas credenciais (geralmente nome de usuário e senha) a um sistema de autenticação (como o Login).
- O servidor de autorização emite um token de acesso: Após autenticação, o servidor gera um token de acesso. Esse token é o que a aplicação usará para acessar os recursos protegidos.
- A aplicação faz chamadas à API com o token de acesso: Com o token, a aplicação consegue fazer solicitações à API protegida sem precisar fornecer a senha do usuário a cada requisição.
- Expiração do token: O token tem um tempo de expiração. Quando expira, o usuário precisa se autenticar novamente para obter um novo token.

## Tipos de Tokens

## Existem diferentes tipos de tokens, sendo os mais comuns:

- Token de acesso (Access Token): Usado para acessar recursos protegidos. Ele é geralmente passado nas requisições HTTP via cabeçalho (Authorization).
- Token de atualização (Refresh Token): Usado para obter um novo token de acesso quando o atual expirar, sem a necessidade de o usuário se autenticar novamente.

## Por que usar OAuth2?

### OAuth2 é altamente seguro e flexível. Ele oferece várias vantagens para o controle de autenticação e autorização em sistemas web e APIs, incluindo:

- Segurança: Ao utilizar tokens de acesso temporários, as credenciais (senhas) dos usuários não precisam ser compartilhadas diretamente, o que reduz o risco de vazamentos.
- Escalabilidade: OAuth2 permite que os usuários autorizem vários serviços sem precisar digitar suas credenciais repetidamente.
- Controle de Acesso: OAuth2 pode ser configurado para permitir que diferentes usuários acessem diferentes níveis de recursos, com base em suas permissões (roles).

## O que este projeto faz?

### Este projeto implementa um sistema de CRUD de usuários com autenticação utilizando OAuth2. A aplicação é construída com o FastAPI, um framework moderno e rápido para APIs, e implementa os seguintes fluxos:

- Cadastro de Usuário: Crie um novo usuário fornecendo nome de usuário, email, senha e papel (role). O password é armazenado de forma segura com hashing.

- Login: Faça login utilizando as credenciais do usuário (nome de usuário e senha), e receba um token de acesso (JWT) que pode ser usado para fazer requisições autenticadas.

- Endpoints protegidos: Apenas usuários autenticados com um token de acesso válido podem acessar informações protegidas, como listar usuários ou alterar dados de um usuário.

- Permissões baseadas em papéis (roles): A aplicação suporta diferentes papéis (roles) para os usuários, como "admin" ou "user". Apenas usuários com papéis adequados podem realizar certas operações, como criar, atualizar ou deletar usuários.

# Como a implementação funciona?
## Arquitetura do OAuth2

- ### Autenticação:
    - O usuário envia suas credenciais (usuário e senha) para o endpoint /token.
    - O sistema valida as credenciais e emite um token JWT (JSON Web Token) de acesso.
    - Este token contém informações importantes, como o nome do usuário e o papel (role).

- ### Proteção de rotas:
    - Para acessar endpoints protegidos, o usuário deve enviar o token JWT no cabeçalho Authorization de cada requisição.
    - O FastAPI valida o token e verifica se o usuário tem permissão para acessar o recurso solicitado.

- ### Verificação de permissões:
    - Além de verificar se o usuário está autenticado (token válido), a aplicação verifica o papel do usuário para permitir ou bloquear o acesso a determinadas rotas.

## Principais Componentes do Código

- ### Modelos de Dados:
    - UserDB: Representa o modelo do usuário no banco de dados. Contém informações como nome de usuário, senha hash, e papel.
    - User: Modelo Pydantic para a validação de entrada e saída de dados relacionados ao usuário.
    - Token: Representa o token de acesso JWT retornado após a autenticação.
    - TokenData: Contém dados extraídos do token (como o nome de usuário e papel).

- ### Funções de Autenticação:
    - authenticate_user: Valida as credenciais de login e retorna o usuário autenticado.
    - create_access_token: Gera um token JWT válido, que é usado para autenticação futura.
    - get_current_user: Recupera o usuário autenticado com base no token JWT fornecido na requisição.
    - verify_permissions: Verifica se o usuário tem permissão (com base no papel) para acessar um recurso.

- ### Rotas (Endpoints):
    - /token: Gera e retorna o token JWT após a autenticação.
    - /users/: CRUD de usuários, com autorização para criar, listar, atualizar ou deletar com base no papel.
    - Endpoints protegidos: Todos os endpoints que exigem autenticação e permissões verificam o token JWT para garantir que o usuário tenha permissão para realizar a ação.

# Exemplos de uso
- ### 1. Criação de um Usuário

### Para criar um novo usuário (apenas permitido para administradores), envie uma requisição POST para /users/ com as informações do usuário (nome de usuário, email, etc.) e a senha.

    POST /users/
    Content-Type: application/json

    {
    "username": "johndoe",
    "full_name": "John Doe",
    "email": "johndoe@example.com",
    "password": "strongpassword123",
    "role": "admin"
    }

- ### 2. Login

### Faça login com o nome de usuário e a senha para obter um token JWT.

    POST /token
    Content-Type: application/x-www-form-urlencoded

    username=johndoe&password=strongpassword123

    Resposta:

    {
    "access_token": "your_jwt_token_here",
    "token_type": "bearer"
    }

- ### 3. Acesso a Endpoints Protegidos

### Para acessar um endpoint protegido (como /users/), envie uma requisição com o token JWT no cabeçalho Authorization.

    GET /users/
    Authorization: Bearer your_jwt_token_here

## Como o projeto simplifica o uso do OAuth2?

Este projeto fornece uma implementação simplificada do OAuth2 com FastAPI, permitindo que você se concentre no desenvolvimento do seu aplicativo sem precisar se preocupar com detalhes complexos de autenticação. O uso de JWT e a validação de permissões baseadas em papéis torna fácil a integração de segurança nas suas APIs.
## Vantagens:

- Implementação fácil e direta: Usando FastAPI, o processo de autenticação com OAuth2 se torna simples de configurar e integrar.
- Validação de permissões: Definir permissões para diferentes papéis de usuários (admin, user) é fácil e flexível.
- Segurança: A aplicação usa JWT para garantir que apenas usuários autenticados com permissões adequadas possam acessar recursos protegidos.

# Conclusão

OAuth2 é uma excelente escolha para implementar autenticação segura e escalável em APIs e aplicações web. Neste projeto, mostramos como usar OAuth2 de maneira simples e eficiente, garantindo que apenas usuários autenticados e autorizados possam acessar recursos protegidos. Com FastAPI, o processo se torna ainda mais rápido e eficiente, permitindo que você implemente autenticação robusta com um mínimo de código.

# Contribuições
Contribuições são bem-vindas! Se você tiver sugestões ou melhorias, sinta-se à vontade para abrir um issue ou enviar um pull request.;)

## Autores
- [@Rodrigo_Kelven](https://github.com/Rodrigo-Kelven)

