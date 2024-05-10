FROM python:3.12.3-alpine3.19

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD echo "${CRON_SCHEDULE}" python3 /app/src/main.py | crontab - && crond -f