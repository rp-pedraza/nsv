FROM tiangolo/uwsgi-nginx:python3.12

# Copy files.
COPY process-templates.bash /etc/nginx/process-templates.bash
COPY server.conf.template /etc/nginx/conf.d/server.conf.template
COPY --from=root frontend/dist/. /usr/share/nginx/html
COPY --from=root frontend/bower_components/. /usr/share/nginx/html/bower_components

# Set command to execute at runtime.
CMD ["/bin/bash", "-c", ". /etc/nginx/process-templates.bash; exec nginx"]
