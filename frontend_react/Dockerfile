FROM node:18-alpine

WORKDIR /app

RUN node -v
RUN npm install -g yarn --force --no-cache
RUN yarn -v
RUN npm install -g typescript --force --no-cache
RUN tsc -v
RUN npm i --save-dev @types/node --no-cache

COPY . .
RUN yarn install --no-cache
RUN yarn install -g http-server --no-cache

#RUN yarn build

EXPOSE 3500

CMD [ "http-server", "./dist", "-p", "3500" " || ", "/bin/sh"]