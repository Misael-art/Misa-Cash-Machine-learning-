# Estágio de build para o frontend
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# Copiar arquivos de configuração
COPY src/web/frontend/package.json src/web/frontend/package-lock.json ./

# Instalar dependências
RUN npm ci

# Copiar código fonte
COPY src/web/frontend/ .

# Construir a aplicação
RUN npm run build

# Estágio de build para o backend
FROM node:18-alpine AS backend-build

WORKDIR /app/backend

# Copiar arquivos de configuração
COPY src/web/backend/package.json src/web/backend/package-lock.json ./

# Instalar dependências
RUN npm ci

# Copiar código fonte
COPY src/web/backend/ .

# Construir a aplicação
RUN npm run build

# Estágio final
FROM node:18-alpine

WORKDIR /app

# Instalar dependências de produção
RUN apk add --no-cache python3 make g++

# Copiar arquivos de configuração
COPY src/web/backend/package.json src/web/backend/package-lock.json ./backend/
COPY src/web/frontend/package.json src/web/frontend/package-lock.json ./frontend/

# Instalar dependências de produção
WORKDIR /app/backend
RUN npm ci --only=production

WORKDIR /app/frontend
RUN npm ci --only=production

# Copiar builds
COPY --from=frontend-build /app/frontend/dist ./dist
COPY --from=backend-build /app/backend/dist ./backend/dist

# Configurar variáveis de ambiente
ENV NODE_ENV=production
ENV PORT=3000

# Expor porta
EXPOSE 3000

# Comando para iniciar a aplicação
CMD ["node", "backend/dist/server.js"] 