FROM python:3.9-slim

WORKDIR /app

WORKDIR /app

RUN apt update \
    && apt install -y --no-install-recommends python3-pip \
    && ln -sf python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip \
    && pip install --upgrade pip uv \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./
RUN uv pip install -r pyproject.toml

CMD []