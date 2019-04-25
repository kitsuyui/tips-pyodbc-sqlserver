FROM python:3.7.3-stretch@sha256:6d0845875c060792cf45793227f7a01d8024624fb83d4d3d75fddd9032b5db1b
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
