FROM python:3.8.6-alpine
WORKDIR /app
RUN apk add --no-cache mariadb-connector-c-dev libffi-dev openssl-dev && \
        apk add --no-cache --virtual .build-deps build-base mariadb-dev && \
        apk add --no-cache --virtual ca-certificates apache2-utils && \
        pip install mysqlclient==2.0.1 && pip install pyopenssl==19.1.0 && \
        apk del .build-deps
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD webcrawler webcrawler
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
CMD [ "python", "-m", "webcrawler" ]