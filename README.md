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

# Run migrations
docker-compose run web python manage.py migrate

# Create superuser (optional)
docker-compose run web python manage.py createsuperuser

# Start all services
docker-compose up