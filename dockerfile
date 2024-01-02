FROM python:3.12.1-slim-bullseye

WORKDIR /asteroids

ADD  asteroids.py .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./asteroids.py" ]