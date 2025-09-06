FROM python:3.13-bookworm AS builder
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  default-mysql-client \
  tzdata \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip setuptools wheel \
  && pip install --no-cache-dir pdm

WORKDIR /project

#
# Production
#
FROM builder

# ファイルは複数列挙で一括コピー可能
COPY pyproject.toml pdm.lock README.md alembic.ini ./

# ディレクトリは1つずつ記述する必要あり
COPY migrations migrations
COPY src src
COPY scripts scripts

RUN mkdir __pypackages__ \
  && pdm install --no-lock --no-editable --prod

#
# Development
#
FROM builder AS development

# `pdm install`に必要なファイルだけをコピー
COPY pyproject.toml pdm.lock README.md ./
COPY src/__init__.py src/__init__.py
COPY scripts scripts
RUN ls /project/scripts/run.sh

RUN mkdir __pypackages__ \
  && pdm install --no-lock --no-editable