FROM node:18-alpine

WORKDIR /app

RUN node -v
#RUN npm install -g yarn --force
#RUN yarn -v
RUN npm install -g typescript --force
RUN tsc -v
RUN npm i --save-dev @types/node

COPY . .
RUN npm install -g "@angular/cli" --no-cache

RUN npm install --no-cache
#RUN npm build

EXPOSE 4000

RUN ng build
CMD [ "ng", "serve", "--host=0.0.0.0", "--port=4000" ]