FROM python:3.8.3-slim-buster

COPY requirements.txt .  

# PYODBC DEPENDENCES
RUN \
    export ACCEPT_EULA='Y' && \
    apt-get update && \
    apt-get install -y curl build-essential tdsodbc unixodbc-dev g++ unixodbc-bin apt-transport-https

# ODBC DRIVER
RUN \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 --assume-yes

 # Update odbcinst.ini 
ADD odbcinst.ini /etc/odbcinst_FreeTDS.ini
RUN \
    cat /etc/odbcinst_FreeTDS.ini /etc/odbcinst.ini > /tmp/temp.ini && \
    mv -f /tmp/temp.ini /etc/odbcinst.ini && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && rm requirements.txt

# Clean up
RUN \
    apt-get remove -y curl apt-transport-https debconf-utils g++ gcc rsync unixodbc-dev build-essential && \
    apt-get autoremove -y && apt-get autoclean -y

# CONFIGURE ENV FOR /bin/bash TO USE MSODBCSQL17
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile 
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc 