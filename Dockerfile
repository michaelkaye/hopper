FROM ubuntu
RUN apt-get update
RUN apt-get install -y python3 python-pip curl netcat
RUN useradd -ms /bin/bash hopper
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /home/hopper/code
WORKDIR /home/hopper/code
ENV DJANGO_SETTINGS_MODULE=hopper.settings
ENV PYTHONPATH=/home/hopper/code/src
USER hopper
