FROM node:18.16 as build
WORKDIR /app
COPY package*.json ./
RUN npm install 
COPY . .
CMD [ "npm","run","start" ]