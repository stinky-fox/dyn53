FROM python:alpine3.19

# Arguments 

ARG BUILD_DATE

ARG BUILD_VERSION

# Labeling an image

LABEL maintainer="stinky-fox"

LABEL org.label-schema.schema-version="1.0"

LABEL org.label-schema.name="DynR53"

LABEL org.label-schema.description="Backend for DyunR53 project - simple way to have dynamic DNS. Initially built for Route 53 AWS but with further expansion to other vendors."

LABEL org.label-schema.url="https://github.com/stinky-fox/dyn53"

LABEL org.label-schema.build-date=$BUILD_DATE

LABEL org.label-schema.version=$BUILD_VERSION


# setting up workdir

WORKDIR /app

# create directory for files needed during the installation

RUN mkdir /install

COPY requirements.txt /install

# install dependencies using pip

RUN pip3 install -r /install/requirements.txt

# copy Python files
COPY *.py /app/

# set run

CMD ["python3", "-u", "main.py"]