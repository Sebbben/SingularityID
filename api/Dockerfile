FROM python:alpine AS base

FROM base AS dev

WORKDIR /app
RUN mkdir src
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./src

EXPOSE 3000
