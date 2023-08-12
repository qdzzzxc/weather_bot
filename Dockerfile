FROM python:3.11
WORKDIR /weather_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
# узнать чо тут
COPY . .
RUN alembic upgrade head
CMD ["python", "m", "bot"]