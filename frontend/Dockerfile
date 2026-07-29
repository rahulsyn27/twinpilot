FROM node:22-alpine

WORKDIR /workspace/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

COPY frontend /workspace/frontend

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0", "--port", "3000"]
