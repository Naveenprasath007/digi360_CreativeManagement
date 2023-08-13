FROM nginx:latest
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Create a directory to store the error log
RUN mkdir /var/log/nginx/errors

# Make sure the Nginx user has write access to the error log directory
RUN chown nginx:nginx /var/log/nginx/errors