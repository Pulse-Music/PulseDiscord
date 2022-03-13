FROM python:3.9.7

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN sudo apt update
RUN sudo apt install -y python3-pip
RUN pip3 install -r requirements.txt
SHELL [ "python", "." ]
