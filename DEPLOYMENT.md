# FALCON Deployment

## Local
1. Create and activate a virtual environment.
2. Install `requirements.txt`.
3. Run `python manage.py migrate`.
4. Run `python manage.py runserver`.

## Render
This project is configured for a Render Web Service.
- Build: `./build.sh`
- Start: `gunicorn travel_agency.wsgi:application --log-file -`
- Set `SECRET_KEY` and `DEBUG=False`.
- Set `ALLOWED_HOSTS` to the Render hostname.
- For persistent production data, configure a PostgreSQL `DATABASE_URL`.

## Demo data
Run `python seed_db.py` locally if you need the sample destinations, packages, guides, and services.
