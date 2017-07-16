FROM python:3.6.1

ENV DJANGO_SETTINGS_MODULE bank-reader.settings.dev
ENV DATABASE_URL postgres://devel:123456@postgres:5432/bank-reader

ENV UWSGI_HTTP 0.0.0.0:8000
ENV UWSGI_PROCESSES 2

WORKDIR /app

COPY ./requirements/dev.txt /app/
RUN pip install -r dev.txt

EXPOSE 8000

CMD ["uwsgi", "--need-app", "--chdir", "django-bank-reader", "--py-autoreload", "1", \
     "--http", "8000", "--module", "bank-reader.wsgi", "--check-static", \
     "/app/django-bank-reader/", "--offload-threads", "4"]
