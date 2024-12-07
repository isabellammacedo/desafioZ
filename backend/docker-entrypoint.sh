#!/bin/sh

until nc -z -v -w30 db 5432; do
  echo "Aguardando o banco de dados ..."
  sleep 1
done

echo "Rodando as migrations ..."
python manage.py migrate

echo "Cadastrando o usuário admin ..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
  User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF

echo "Servidor inicializado com sucesso ..."
exec "$@"