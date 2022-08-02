FROM python:3.9-alpine
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#COPY ./app /code/app
#COPY ./ssl /code/ssl
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--ssl-keyfile=./ssl/key.pem", "--ssl-certfile=./ssl/certificate.pem"]