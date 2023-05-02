FROM python:3.10.6
COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src
WORKDIR src
EXPOSE 8080
# copy project
COPY . .
