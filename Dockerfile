FROM python:3
LABEL authors="kostik80_80@mail.ru"
WORKDIR /content_platform
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .