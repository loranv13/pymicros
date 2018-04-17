FROM python:latest

RUN apt-get update

RUN pip3 install stomp.py
RUN pip3 install kazoo

RUN mkdir /micro/
RUN mkdir /micro/etc/
RUN mkdir /micro/filegen/
RUN mkdir /micro/pymicros/


COPY etc/ /micro/etc/
COPY example.py  /micro/
COPY filegen/  /micro/filegen/ 
COPY pymicros/ /micro/pymicros/


RUN ls -la /micro
WORKDIR /micro
CMD ["python", "./example.py"]
