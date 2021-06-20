FROM nginx

# удаление настроек по умолчанию
RUN rm /etc/nginx/conf.d/default.conf

# копирование настроек nginx
COPY nginx.conf /etc/nginx/conf.d
