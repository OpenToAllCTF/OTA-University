FROM python:3.6

RUN apt-get update && apt-get install -y chromium libgtk-3-0

RUN mkdir /app
RUN adduser app --disabled-login --disabled-password

WORKDIR /app

COPY ./src/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src .

RUN chown -R app:app /app
USER app

CMD ["hypercorn", "--bind", ":5000", "main:app"]