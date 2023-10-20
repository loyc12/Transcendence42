FROM node:18-alpine

WORKDIR /app

RUN node -v
RUN npm install -g yarn --force --no-cache
RUN yarn -v
RUN npm install -g typescript --force --no-cache
RUN tsc -v
RUN npm i --save-dev @types/node --no-cache
RUN mkdir dist


COPY . .
RUN yarn install --no-cache

RUN yarn build


EXPOSE 3000

ENTRYPOINT [ "./tools/entrypoint.sh" ]

CMD [ "yarn", "run", "start:dev" ]