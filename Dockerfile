FROM python:3.7.2-stretch@sha256:d080febec9e26885db2e569d2dee9bd0b1117fb2e219241ac33d118887f7cb94
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
