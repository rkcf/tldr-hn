FROM alpine:3.8

# Install build deps
RUN apk add --no-cache python3 gcc musl-dev python3-dev linux-headers libxml2-dev libxslt-dev libjpeg-turbo-dev\
	&& pip3 install --no-cache-dir --upgrade pip

# Create user
WORKDIR /var/www
RUN adduser -D -s /sbin/nologin -h /var/www uwsgi

# Install app deps
COPY requirements.txt /var/www
RUN pip install --no-cache-dir -r requirements.txt

# Install nltk data
RUN python3 -m nltk.downloader -d /var/www/nltk_data punkt

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

# Add source to container
COPY tldrhn /var/www/tldrhn
RUN chown -R uwsgi:uwsgi /var/www

USER uwsgi
ENTRYPOINT docker-entrypoint.sh
