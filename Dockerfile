FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
COPY src ./src
COPY server.js ./server.js
ENV PORT=4173
EXPOSE 4173
CMD ["node", "server.js"]
