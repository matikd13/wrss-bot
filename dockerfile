FROM python:3.12

LABEL Maintainer="wrss.wiet"

WORKDIR /app

COPY wrss-bot.py /app
COPY config.py /app
COPY requirements.txt /app 

RUN python3 -m pip install -r requirements.txt

CMD [ "python", "./wrss-bot.py"]
