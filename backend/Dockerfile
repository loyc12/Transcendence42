FROM node:18

WORKDIR /app

RUN node -v
RUN npm install -g yarn --force
RUN yarn -v
RUN npm install -g typescript --force
RUN tsc -v
RUN npm i --save-dev @types/node

COPY package*.json ./

RUN yarn install

COPY . .

RUN yarn build

CMD [ "yarn", "run", "start:dev" ]