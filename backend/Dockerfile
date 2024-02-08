FROM python:3.11

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . ./

CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload