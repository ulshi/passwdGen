FROM python:3.6-alpine
COPY . /src
WORKDIR /src
RUN pip install Django log pymysql SQLAlchemy
RUN apk --no-cache add zeromq && adduser -s /bin/false -D django
COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages
COPY --from=builder /usr/local/bin/locust /usr/local/bin/locust
COPY docker_start.sh docker_start.sh
RUN chmod +x docker_start.sh

EXPOSE 8000

USER django
CMD ["./python3 manage.py runserver 0.0.0.0:8000"]
