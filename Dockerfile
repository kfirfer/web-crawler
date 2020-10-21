FROM openkbs/jre-mvn-py3

ENV USER_ID=${USER_ID:-1000}
ENV GROUP_ID=${GROUP_ID:-1000}
ENV USER=${USER:-developer}
ENV HOME=/home/${USER}

USER root
RUN mkdir -p /opt/firefox
RUN mkdir -p /app

RUN apt-get update && apt-get install -y libmysqlclient-dev default-libmysqlclient-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev

# And of course we need Firefox if we actually want to *use* GeckoDriver
RUN set -xe \
    &&  wget --no-check-certificate --quiet --output-document - \
        'https://download.mozilla.org/?product=firefox-esr-latest-ssl&os=linux64&lang=en-US' | \
        tar --extract --bzip2 --directory /opt \
    &&  ln --symbolic /opt/firefox/firefox /opt/firefox/firefox-esr

ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

USER ${USER}
ADD mobilenium mobilenium
ADD webcrawler webcrawler
USER root
RUN chown -R ${USER}:${USER} /app
USER ${USER}
CMD [ "python3", "-m", "webcrawler" ]