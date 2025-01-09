FROM python:3.14.0a3-alpine3.20

COPY ./src /usr/app
COPY ./requirements.txt /usr/app

RUN apk update && apk add gzip

WORKDIR /usr/app

RUN pip install --upgrade pip && pip install -r requirements.txt
RUN mkdir /usr/app/output

ADD https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2025-01-01_anthem_index.json.gz /usr/app/input/
RUN gzip -d /usr/app/input/2025-01-01_anthem_index.json.gz

ENTRYPOINT [ "python", "main.py"]
CMD ["/usr/app/input/2025-01-01_anthem_index.json"]
