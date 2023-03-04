FROM python:3.9.4-alpine
LABEL maintainer="Romaric Yemeli"
WORKDIR /opt
RUN apk update && \
    apk add gcc musl-dev postgresql-dev bash
RUN pip install --upgrade pip
COPY . /opt/
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["python","manage.py","runserver","0.0.0.0:80"]