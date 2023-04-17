FROM python:3.10.6
COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt
COPY . /src
WORKDIR src
EXPOSE 6060

COPY ./entrypoint.sh .
RUN chmod +x /src/entrypoint.sh
# copy project
COPY . .

# run entrypoint.sh
RUN bash entrypoint.sh