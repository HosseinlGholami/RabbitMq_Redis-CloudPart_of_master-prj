FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY log.txt ./log/
COPY main.py ./
COPY util.py ./


CMD [ "python", "./main.py" ]

