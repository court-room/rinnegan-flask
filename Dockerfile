FROM python:3.8.5 as builder

LABEL maintainer="onlinejudge95"

WORKDIR /usr/src/app

COPY ./Pipfile ./

RUN pip install pipenv==2018.11.26 \
    && pipenv lock --requirements > ./requirements.txt \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels --requirement ./requirements.txt

##############################################################################

FROM python:3.8.5-slim-buster

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install libpq-dev=11.7-0+deb10u1 libpq5=11.7-0+deb10u1 wget -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/src/app/wheels /wheels

RUN pip install --no-cache-dir /wheels/*

COPY . .

RUN chmod +x bin/entrypoint.sh

CMD [ "./bin/entrypoint.sh" ]
