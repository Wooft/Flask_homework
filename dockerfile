FROM python:3.10.6
COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src
EXPOSE 6060
WORKDIR src
RUN gunicorn --bind 127.0.0.1:5000 server:app
