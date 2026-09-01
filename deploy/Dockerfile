# Serve the Pearl & Co. scroll-world static demo with nginx.
FROM nginx:1.27-alpine
COPY demo/ /usr/share/nginx/html/
# Enable byte-range friendly caching hints for media
COPY deploy/nginx-default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
