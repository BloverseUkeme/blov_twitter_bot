FROM python:3.10.2-slim-buster 
#FROM python:3.7.5-slim-buster


ENV INSTALL_PATH /twitterbot
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -c "python:config.gunicorn" "twitterbot.app:create_app()"
