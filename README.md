# dteam-test
## **Loading Fixtures**
To load sample data into a DB:
```bash
python manage.py loaddata cv.json

brew install cairo pango gdk-pixbuf libffi

GET /api/cvs/ - List all CVs

POST /api/cvs/ - Create new CV

GET /api/cvs/{id}/ - Retrieve single CV

PUT/PATCH /api/cvs/{id}/ - Update CV

DELETE /api/cvs/{id}/ - Delete CV


Check the logs on /admin/ with admin admin

Check the settings on /settings/

# Build containers
docker-compose build 

or

docker-compose up -d --build


# Run migrations
docker-compose run web python manage.py migrate

# Create superuser (optional)
docker-compose run web python manage.py createsuperuser

# Start all services
docker-compose up


#Start celery and redis
celery -A CVProject  worker --loglevel=info
brew services start redis

#DigitalOcean connect via ssh key

# Update packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl git
sudo apt install -y redis-server
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo apt install -y certbot python3-certbot-nginx
sudo apt install -y libpango-1.0-0 libpango1.0-dev libcairo2 libcairo2-dev libgdk-pixbuf2.0-0 libgdk-pixbuf2.0-dev libffi-dev shared-mime-info

usermod -aG sudo django

# Create PostgreSQL database and user
sudo -u postgres psql
CREATE DATABASE cvprojectdb;
CREATE USER myprojectuser WITH PASSWORD 'password';
ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myprojectuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE cvprojectdb TO myprojectuser;
\q

# Create a system user for your app
sudo adduser --disabled-password --gecos "" django

# Install virtualenv
sudo -H pip3 install virtualenv

# As django user
sudo su - django
mkdir ~/app && cd ~/app


# Clone your project (or use SCP to transfer files)
git clone https://github.com/sergeyitaly/dteam-test .
python3 -m virtualenv venv
source venv/bin/activate

pip install -r requirements.txt


nano CVProject/settings/production.py
#add this ...
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['your_domain_or_ip']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=django
Group=www-data
WorkingDirectory=/home/django/app
ExecStart=/home/django/app/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/django/app/app.sock CVProject.wsgi:application

[Install]
WantedBy=multi-user.target


#tart gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

sudo nano /etc/nginx/sites-available/CVProject

sudo ln -s /etc/nginx/sites-available/CVProject /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx