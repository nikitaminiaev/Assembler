FROM python:3.7-alpine

COPY requirements.txt /
COPY . /usr/src/app

RUN pip install -r /requirements.txt

WORKDIR /usr/src/app

EXPOSE 8266

ENTRYPOINT ["python", "main.py"]