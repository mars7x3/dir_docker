FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/Dir
COPY ./rex.txt /usr/src/rex.txt
RUN pip install -r /usr/src/rex.txt

COPY . /usr/src/Dir

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
