FROM python:3.7.3-stretch@sha256:205cafadbb7f0c48f2a6d655eb100a9675aa85e6e73958860f488406cce09779
RUN \
DEBIAN_FRONTEND=noninteractive \
apt-get update && \
apt-get install -y apt-transport-https && \
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
apt-get update && \
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev
ADD requirements.txt /
RUN pip3 install -r requirements.txt
