# pynanabot
Bananabot using Django REST framework

## Execution

### docker compose (recommended)

1. `docker-compose up`
2. Add `-d` option to detach terminal
3. Add `--build` option to rebuild docker image

### docker run

1. `docker build -t pynanabot .`
2. `docker run -p [outbound port number]:8000 --name pynanabot_service pynanabot`

### Local

1. `python3 -m venv env` (python3.12 recommended)
2. `source env/bin/activate`
3. `pip install -r requirements.txt`
4. set .env file appropriately (django secret key)
5. `python manage.py createsuperuser --username admin --email admin@example.com` (optional)
6. `python3 manage.py migrate`
7. `python3 manage.py runserver 0.0.0.0:[port number]` for outbound connection
