#!/bin/bash

echo "Waiting for mysql to start..."
until mysql $MYSQL_DATABASE -h$MYSQL_HOST -u$MYSQL_USER -p$MYSQL_PASSWORD &>/dev/null
do
	sleep 1
done

echo "Start migration"
# 自動マイグレーションを追加
cd /project && pdm run alembic upgrade head
echo "Done migration"

echo "Start api server"
cd /project && \
  pdm run uvicorn src.main:app --reload --port=8000 --host=0.0.0.0
