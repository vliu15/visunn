FROM python:3.7.7-slim

WORKDIR /

RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y graphviz tk

RUN pip install \
    torch==1.4.0+cpu \
    torchvision==0.5.0+cpu \
 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install -r requirements.txt
