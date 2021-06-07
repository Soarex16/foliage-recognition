FROM node:14-alpine as deps

WORKDIR /app

COPY package.json ./
COPY package-lock.json ./
RUN npm ci

FROM deps as base
COPY . .

FROM base AS dev
ARG NODE_ENV=development
ENV NODE_ENV $NODE_ENV
CMD npm run dev

FROM base AS build
ENV NODE_ENV $NODE_ENV
ARG NODE_ENV=production
RUN npm run build

FROM nginx:1.19-alpine AS prod
# Add bash
RUN apk add --no-cache bash

COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
# Copy script that generates env variables js file
COPY --from=build /app/scripts/generate-env-file.sh /
RUN chmod +x /generate-env-file.sh
COPY --from=build /app/dist/ /usr/share/nginx/html

# Start Nginx
CMD ["/bin/ash", "-c", "/generate-env-file.sh -o /usr/share/nginx/html && nginx -g \"daemon off;\""]
