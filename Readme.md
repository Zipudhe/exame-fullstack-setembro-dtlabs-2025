# Case Fullstack dt-labs

<!--toc:start-->
- [Case Fullstack dt-labs](#case-fullstack-dt-labs)
  - [API (FastAPI)](#api-fastapi)
  - [Frontend (React)](#frontend-react)
  - [Infra(Docker/docker-compose)](#infradockerdocker-compose)
  - [Instrução de Uso](#instrução-de-uso)
    - [Backend](#backend)
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

## Instrução de Uso

### Backend

- para rodar a aplicação do backend check a as variáveis de ambiente necessárias
- Com as variáveis configuradas rode o comando
  bash```
    docker-compose up

  ```
  - Com os serviços rodando caso seja necessário rode o comando de seed da api 
    bash```
        docker exec <container-name> python3 -m config.seed
      ```

### Frontend - Setup Instructions

#### Instalação

#### 1. Clone o repositório

```bash
git clone https://github.com/Zipudhe/exame-fullstack-setembro-dtlabs-2025.git
cd exame-fullstack-setembro-dtlabs-2025/frontend
```

#### 2. Instale as dependências

```bash
npm install
```

Or using yarn:

```bash
yarn install
```

### 3. Environment Configuration

Crie as variaveis de ambiente `.env` no diretório do frontend:

```bash
cp .env.example .env
```

Ou crie um do zero :

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## Running the Application

### Development Mode

Servidor de desenvolvimento:

```bash
npm run dev
```

Or with yarn:

```bash
yarn dev
```

A Aplicação vai rodar por padrão em: `http://localhost:3000`.

### Production Build

To create an optimized production build:

```bash
npm run build
```

Or with yarn:

```bash
yarn build
```

This creates a `build` folder with optimized production files.

## Estrutura do projeto

```
frontend/
├── public/          # Static files
├── src/
│   ├── components/  # React components
│   ├── pages/       # Page components
│   ├── services/    # API services
│   ├── utils/       # Utility functions
│   ├── App.js       # Main App component
│   └── index.js     # Entry point
├── .env             # Environment variables
├── package.json     # Dependencies and scripts
└── README.md        # This file
```

## Scripts disponíveis

| Command | Description |
|---------|-------------|
| `npm start` | Runs the app in development mode |
| `npm test` | Launches the test runner |
| `npm run build` | Builds the app for production |
| `npm run eject` | Ejects from Create React App (irreversible) |

## Troubleshooting

### Dependencies Issues

Em caso de conflitos:

```bash
npm cache clean --force

rm -rf node_modules package-lock.json
npm install
```

## Backend Connection

Essa aplicação frontend requer conexão com API, certifique que:

1. O backend server está rodando (Por padrão na URL `http://localhost:8000`)
2. As variáveis de ambiente estão configuradas `.env` apontam para backend URL
3. CORS está configurado corretametne

[backend README](../backend/README.md) pra backend setup.

## Tecnologias Utilizadas

- React
- React Router
- Axios
- WebSocket
- CSS Modules / Styled Components / Tailwind

## Tarefas

- [x] Criar repositório (Monolito)
- [x] Definir banco de dados
  - [x] Criar Dockerfile para ele
- [x] Criar projeto FastAPI
- [ ] Criar projeto React
- [ ] Definir Infra
- [x] Estrutura de testes

### Tarefas Frontend

- [x] Criar pagina de login
- [x] Criar pagina Home
- [x] Criar pagina de listagem de devices
  - [ ] Criar modelos de gráficos
- [ ] Criar pagina de edição de devices
- [ ] Criar pagina listagem notificacoes
- [ ] Criar pagina de edição de notificacoes

### Tarefas API

- [x] Usuario padrão para testes
- [x] Criar rota de login de usuário
- [x] Criar rotas dispostivos
  - [x] listagem completa com filtros (paginacão)
  - [x] listagem resumida (CPU, RAM e Temp) (paginacão)
- [x] Criar rotas de notificações
  - [x] Listagem de notificações
  - [x] Criar de notificação
  - [x] Editar de notificação
  - [x] Remover notificação
- [x] Criar rota de edição de dispostivos
- [x] Configurar logger

## Histórias do Usuário

- [x] Criar rota de login para usuarios
- [x] Como usuario quero poder ter acesso a uma listagem dos meus
  dispostivos
- [x] Como usuario quero um resumo dos status de CPU, RAM e temperatura dos dispostivos
- [x] Como usuario quero ser capaz de filtrar meus dispostivos
- [x] Como usuário quero ver gráficos do histórico de dados de heartbeats
- [x] Como usuário quero ser capaz de filtrar período de histórico
- [x] Como usuário quero ser capaz de criar notificações baseado nos status de dispostivos
- [x] Como usuário quero ser capaz de visualizar minhas notificações criadas.
- [ ] Como usuário quero receber notificações em tempo real
de acordo com minhas notificações configuradas
- [x] Como usuário quero registrar novos dispostivos
- [x] Como usuário quero editar meus dispostivos
- [x] Como usuário quero remover dispostivos

## Stack

- React + better-auth
- FastAPI + MongoDB + Redis Streams
