FROM python:3.5

# Change user to 'root'.
USER root

# Install uwsgi.
RUN pip install uwsgi

# Install requirements.
COPY requirements.txt /var/tmp/requirements.txt
RUN pip install -r /var/tmp/requirements.txt; rm /var/tmp/requirements.txt

# Add 'backend' user.
RUN useradd backend -d /dev/null -s /sbin/nologin

# Install application to /app.
RUN mkdir /app
COPY application.py /app/application.py
COPY config.py /app/config.py
RUN chown backend:backend /app -R

# Change user to 'backend'.
USER backend

# Change working directory to '/app'.
WORKDIR /app

# Expose port 5001 to other services.
EXPOSE 5001

# Set the command to execute at runtime.
# To debug with html, add '--http-socket 0.0.0.0:5000'.  You also need to publish the port.
CMD exec /usr/local/bin/uwsgi --master --wsgi-file application.py --callable app --threads 2 --socket 0.0.0.0:5001
