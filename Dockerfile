FROM python:3.11.0-alpine3.16

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

ENV APP_HOST="0.0.0.0"
ENV APP_PORT="8080"

USER daemon
ENTRYPOINT [ "python" ]
CMD [ "routes.py" ]