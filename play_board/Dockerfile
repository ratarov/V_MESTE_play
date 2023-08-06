FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "play_board.wsgi:application", "--bind", "0:8000" ]