FROM python:3.8.3-alpine
WORKDIR /app
RUN apk add --no-cache mariadb-connector-c-dev libffi-dev openssl-dev && \
        apk add --no-cache --virtual .build-deps build-base mariadb-dev && \
        pip install mysqlclient==2.0.0 && \
        apk del .build-deps
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD webcrawler webcrawler
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
CMD [ "python", "-m", "webcrawler" ]