FROM python:3.11.0-alpine3.16

WORKDIR /app
COPY requirements.txt .
RUN chown daemon /app && pip install -r requirements.txt
COPY . .

ENV APP_HOST="0.0.0.0"
ENV APP_PORT="8080"

EXPOSE 8080

USER daemon

ENTRYPOINT [ "gunicorn" ]
CMD [ "routes:app", "-b", "0.0.0.0:8080", "--log-file", "-", "--access-logfile", "-", "--workers", "4", "--keep-alive", "0" ]
