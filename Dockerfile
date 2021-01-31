FROM python:3.7.2-slim

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y \
    python3-tk
RUN mkdir /usr/src/app
COPY requirements.txt /usr/src/app
WORKDIR /usr/src/app
RUN pip install -r /usr/src/app/requirements.txt

COPY . /usr/src/app

ENTRYPOINT ["python", "main.py"]