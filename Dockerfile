FROM python:3.8

EXPOSE 8080

WORKDIR /app
ADD . /app

RUN pip3 install pipenv
RUN pipenv install

CMD [ "pipenv", "run", "python", "main.py" ]