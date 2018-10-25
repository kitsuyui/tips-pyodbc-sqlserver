FROM python:3.7.1-stretch@sha256:719d83ccfaea28f95ca49e157e0fb1267dba84ee84a25a12681f77afa4292db3
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
