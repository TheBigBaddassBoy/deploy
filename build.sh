#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='coron').exists():
    User.objects.create_superuser('coron', 'coron@example.com', 'sahid15')
    print('Superusuario coron creado con éxito.')
else:
    print('El superusuario coron ya existe.')" | python manage.py shell
