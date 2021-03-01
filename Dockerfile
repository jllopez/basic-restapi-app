FROM python:3.7 as base

WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
