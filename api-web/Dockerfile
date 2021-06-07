FROM python:3.8-slim-buster as base

RUN mkdir /svc
COPY requirements.txt /svc
WORKDIR /svc

RUN pip install wheel && pip wheel --wheel-dir=/svc/wheels -r requirements.txt

FROM python:3.8-slim-buster as final

WORKDIR /app
COPY . /app
COPY --from=base /svc/wheels /svc/wheels

RUN pip install --upgrade pip; \
    pip install --no-index --find-links=/svc/wheels -r requirements.txt

CMD ["python", "main.py"]