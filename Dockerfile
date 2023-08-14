FROM python:3.11
WORKDIR /weather_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .