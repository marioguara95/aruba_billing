FROM node:20
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN npm fund
COPY . .
CMD ["ng","serve"]
