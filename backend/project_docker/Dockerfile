FROM python:3.10
RUN apt-get update && apt-get -y install apt-utils postgresql-client binutils libgdal-dev libproj-dev gdal-bin postgis netcat screen nano sudo rsync
ENV APP_HOME=/home/chat_gpt_api
RUN mkdir -p $APP_HOME
RUN useradd -G sudo -U -M -d $APP_HOME app
WORKDIR $APP_HOME
COPY etc /etc/
RUN chown app:app $APP_HOME -R
USER app
RUN export LC_ALL="pt_BR.UTF-8"
RUN export LC_CTYPE="pt_BR.UTF-8"
RUN export TERM=xterm