# We can't use 'nginx' image.  The 'uwsgi' module doesn't seem to work in it.
# This 'buildpack-deps:jessie' image is a dependency of 'python:3.5', which
# is the base image of the backend.
FROM buildpack-deps:jessie

# Copied from https://github.com/tiangolo/uwsgi-nginx-docker/blob/master/python3.5/Dockerfile.
# --------------------------------------------------
# Standard set up Nginx
ENV NGINX_VERSION 1.9.11-1~jessie

RUN apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 \
	&& echo "deb http://nginx.org/packages/mainline/debian/ jessie nginx" >> /etc/apt/sources.list \
	&& apt-get update \
	&& apt-get install -y ca-certificates nginx=${NGINX_VERSION} gettext-base \
	&& rm -rf /var/lib/apt/lists/*

# Forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443
# Finished setting up Nginx

# Remove default configuration from Nginx
RUN rm /etc/nginx/conf.d/default.conf
# --------------------------------------------------

# Copy files.
COPY process-templates.sh /etc/nginx/process-templates.sh
COPY server.conf.template /etc/nginx/conf.d/server.conf.template
COPY html /usr/share/nginx/html

# Set command to execute at runtime.
# This would process configuration tempaltes, and execute nginx.
# Images that may try to work on top of this image can override this
# command.  They can choose to call '. /etc/nginx/process-templates.sh'
# or not at their volition.
CMD ["/bin/bash", "-c", ". /etc/nginx/process-templates.sh; exec nginx -g 'daemon off;'"]
