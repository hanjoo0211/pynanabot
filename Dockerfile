FROM python:3.12

# Set the working directory
WORKDIR /pynanabot

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . /pynanabot

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
