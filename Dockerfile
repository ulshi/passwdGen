FROM python:3.6-alpine
COPY . /src
WORKDIR /src
RUN pip3 install Django log pymysql SQLAlchemy

EXPOSE 8000

USER django
CMD ["python3 manage.py runserver 0.0.0.0:8000"]
