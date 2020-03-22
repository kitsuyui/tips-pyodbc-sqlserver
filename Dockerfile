FROM python:3.8.0b1-stretch@sha256:687124fffbd43bcdba83e1db4d7dae93bbd9bbae2e56a1796231d544c30f0833
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
