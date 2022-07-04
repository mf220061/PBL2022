FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app
ENV FLASK_APP=app

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev bash

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#ENTRYPOINT ["python"]
#CMD ["rest.py"]
