FROM node:18-alpine

WORKDIR /app

RUN node -v
RUN npm install -g yarn --force --no-cache
RUN yarn -v
RUN npm install -g typescript --force --no-cache
RUN tsc -v
RUN npm i --save-dev @types/node --no-cache

COPY . .
WORKDIR /app/frontend_vite_react

RUN yarn install --no-cache
#RUN yarn install -g http-server --no-cache
RUN npm run build
#RUN yarn install vite --no-cache
#RUN yarn build

EXPOSE 5173

CMD [ "npm" , "run", "dev", "--", "--host"]
#CMD [ "http-server", "./dist", "-p", "3500" " || ", "/bin/sh"]