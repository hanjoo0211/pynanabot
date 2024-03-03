# pynanabot
Bananabot using Django REST framework

1. `python3 -m venv env` (python3.12 recommended)
2. `source env/bin/activate`
3. `pip install -r requirements.txt`
4. set .env file appropriately (django secret key)
5. `python manage.py createsuperuser --username admin --email admin@example.com` (optinal)
6. `python3 manage.py migrate`
7. `python3 manage.py runserver 0.0.0.0:[port number]` for outbound connection
