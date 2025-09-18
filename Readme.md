# Case Fullstack dt-labs

<!--toc:start-->
- [Case Fullstack dt-labs](#case-fullstack-dt-labs)
  - [API (FastAPI)](#api-fastapi)
  - [Frontend (React)](#frontend-react)
  - [Infra(Docker/docker-compose)](#infradockerdocker-compose)
  - [Tarefas](#tarefas)
    - [Tarefas Frontend](#tarefas-frontend)
    - [Tarefas API](#tarefas-api)
  - [Histórias do Usuário](#histórias-do-usuário)
  - [Stack](#stack)
<!--toc:end-->

## API (FastAPI)

- Acesso de usuarios com suas respectivas senhas (hashed)
- CRUD de usuarios
- CRUD de devices
- CRUD de configuracao de notificacoes
- CRUD Heartbeats

## Frontend (React)
  
- Paginas
  - Publicas
    - Login
  - Privadas
    - Home
    - Devices
    - Notificacoes
    - Registro de Devices

## Infra(Docker/docker-compose)

- Sistema de notificações
- heartbeats (Docker para simular dispostivos)
  - Uso de CPU em %
  - Uso de RAM em %
  - Espaço livre de disco em %
  - Temperatura em graus celcius
  - Latência DNS em ms
  - Conectividade
    - 0 caso não tenha conexão com o DNS
    - 1 caso tenha conexção com o DNS

## Tarefas

- [x] Criar repositório (Monolito)
- [x] Definir banco de dados
  - [x] Criar Dockerfile para ele
- [x] Criar projeto FastAPI
- [ ] Criar projeto React
- [ ] Definir Infra
- [x] Estrutura de testes

### Tarefas Frontend

- [ ] Criar pagina de login
- [ ] Criar pagina Home
- [ ] Criar pagina de listagem de devices
  - [ ] Criar modelos de gráficos
- [ ] Criar pagina de edição de devices
- [ ] Criar pagina listagem notificacoes
- [ ] Criar pagina de edição de notificacoes

### Tarefas API

- [ ] Usuario configurável padrão para testes
- [x] Criar rota de login de usuário
- [ ] Criar rotas dispostivos
  - [ ] listagem completa com filtros (paginacão)
  - [ ] listagem resumida (CPU, RAM e Temp) (paginacão)
- [ ] Criar rotas de notificações
  - [ ] Listagem de notificações
  - [ ] Criar de notificação
  - [ ] Editar de notificação
  - [ ] Remover notificação
- [ ] Criar rota de edição de dispostivos
- [x] Configurar logger

## Histórias do Usuário

- [x] Criar rota de login para usuarios
- [ ] Como usuario quero poder ter acesso a uma listagem dos meus
  dispostivos
- [ ] Como usuario quero um resume dos status de CPU, RAM e temperatura dos dispostivos
- [ ] Como usuario quero ser capaz de filtrar meus dispostivos
- [ ] Como usuário quero ver gráficos do histórico de dados de heartbeats
- [ ] Como usuário quero ser capaz de filtrar período de histórico
- [ ] Como usuário quero ser capaz de criar notificações baseado nos status de dispostivos
- [ ] Como usuário quero ser capaz de visualizar minhas notificações criadas.
- [ ] Como usuário quero receber notificações em tempo real
de acordo com minhas notificações configuradas
- [ ] Como usuário quero registrar novos dispostivos
- [ ] Como usuário quero editar meus dispostivos
- [ ] Como usuário quero remover dispostivos

## Stack

- React + better-auth
- FastAPI + MongoDB + Redis Streams
