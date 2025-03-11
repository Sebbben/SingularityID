FROM python:alpine AS base

FROM base AS dev

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000
