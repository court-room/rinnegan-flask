FROM python:3.8.5 as builder

LABEL maintainer="onlinejudge95<onlinejudge95@gmail.com>"

WORKDIR /usr/src/app

COPY ./Pipfile ./

RUN pip install pipenv==2018.11.26 && \
    pipenv lock --requirements > ./requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement ./requirements.txt

##############################################################################

FROM python:3.8.5-slim-buster

WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY . .

RUN chmod +x bin/entrypoint.sh

CMD [ "./bin/entrypoint.sh" ]
