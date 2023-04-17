# Backend API for Hackathon Submission Platform

Note: This project is not meant to be complete or production ready.

## Setup

```bash
pip install -r requirements.txt
```

## Set Environment Variables

```bash
cp .env.example .env
nano .env
```

## Setup

#### Migrate

```bash
python manage.py migrate
```

#### Create Superuser

```bash
python manage.py createsuperuser
```

## Run

```bash
python manage.py runserver
```

## API Documentation

### Authentication

POST http://127.0.0.1:8000/api/auth/login/ - Login

GET http://127.0.0.1:8000/api/auth/logout/ - Logout

### Hackathons

GET http://127.0.0.1:8000/api/hackathons/ - List all hackathons
GET http://127.0.0.1:8000/api/hackathons/?is_registered=true - List all hackathons

POST http://127.0.0.1:8000/api/hackathons/ - Create a new hackathon (admin | can_add_hackathon permission)

GET http://127.0.0.1:8000/api/hackathons/{hackathon_id}/ - Get a hackathon by id

PUT http://127.0.0.1:8000/api/hackathons/{hackathon_id}/ - Update a hackathon by id (admin | can_update_hackathon
permission)

DELETE http://127.0.0.1:8000/api/hackathons/{hackathon_id}/ - Delete a hackathon by id (admin | can_delete_hackathon
permission)

### Registration

POST http://127.0.0.1:8000/api/hackathons/{hackathon_id}/register/ - Register for a hackathon

### Submissions

GET http://127.0.0.1:8000/api/hackathons/{hackathon_id}/submission/ - Retrieve submission made by the user for a
hackathon

POST http://127.0.0.1:8000/api/hackathons/{hackathon_id}/submission/ - Create submission for a hackathon

PUT http://127.0.0.1:8000/api/hackathons/{hackathon_id}/submission/ - Update submission for a hackathon

DELETE http://127.0.0.1:8000/api/hackathons/{hackathon_id}/submission/ - Delete submission for a hackathon

GET http://127.0.0.1:8000/api/hackathons/{hackathon_id}/submission/all/ - Retrieve all submissions for a hackathon (
admin | can_add_hackathon permission)
