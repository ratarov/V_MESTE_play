FROM python:3.9-slim

RUN apt-get update &&\
    apt-get upgrade -y
    # apt-get upgrade -y &&\
    # apt-get install -y libpq-dev gcc netcat

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

RUN chmod +x run_app.sh

ENTRYPOINT ["/app/run_app.sh"]

# CMD ["gunicorn", "play_board.wsgi:application", "--bind", "0:8000" ]