FROM nginx:alpine

COPY ./modules /usr/share/nginx/html/modules
COPY ./images /usr/share/nginx/html/images

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]