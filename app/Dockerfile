FROM python:3.6

LABEL maintainer "Jacob See <jasee@redhat.com>"

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r app/requirements.txt

CMD ["gunicorn", "--bind=0.0.0.0:5000", "app.wsgi:app"]

EXPOSE 5000
