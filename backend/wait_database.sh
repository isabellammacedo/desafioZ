#!/bin/sh

until nc -z -v -w30 db 5432; do
  echo "Aguardando o bd ..."
  sleep 1
done

echo "Rodando as migrations ..."
python manage.py migrate

echo "Servidor inicializado com sucesso!"
exec "$@"