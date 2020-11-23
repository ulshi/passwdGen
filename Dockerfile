FROM python:3.6-alpine
COPY . /src
WORKDIR /src
RUN python3 install Django log pymysql SQLAlchemy
RUN apk --no-cache add zeromq && adduser -s /bin/false -D django

EXPOSE 8000

USER django
CMD ["python3 manage.py runserver 0.0.0.0:8000"]
