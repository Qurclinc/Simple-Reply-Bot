FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod 755 /app/start.sh

ENTRYPOINT [ "./start.sh" ]