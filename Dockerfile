#FROM python:3.6-alpine
FROM harbor.vimpelcom.ru/dockerhub/library/python:3.6-alpine
RUN pip install flask elasticsearch
WORKDIR ./app
COPY ./app.py ./app/app.py
EXPOSE 5000
ENTRYPOINT python app/app.py
