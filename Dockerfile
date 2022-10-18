FROM carlosornelasti/spark-operator-321:latest
LABEL Mantainers: Carlos Ornelas
  
# Using root user
USER root:root
 
# Create directory for apps
RUN mkdir -p /app

RUN apt-get --allow-releaseinfo-change-suite update && apt-get install -y --no-install-recommends \
    git \
    sudo

RUN apt-get install procps -y

RUN apt-get update && \
    apt install -y python3 python3-pip && \
    pip3 install --upgrade pip setuptools && \
    # Removed the .cache to save space
    rm -r /root/.cache && rm -rf /var/cache/apt/*
 
RUN rm -rf /var/lib/apt/lists/*

# Update Alternatives
RUN sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# Build Arguments
ARG buildtime_ci=default_value \
    buildtime_cs=default_value

# Encoding and connections
ENV PYTHONIOENCODING=utf8 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    AWS_ACCESS_KEY_ID=$buildtime_ci \
    AWS_SECRET_ACCESS_KEY=$buildtime_cs

# Copy jars folder (delta)
COPY ./jars/ /opt/spark/jars/

# Set work directory
#WORKDIR /app

# Copy requirements.txt and install
COPY requirements.txt .
RUN pip3 install --no-cache -r requirements.txt

#Copy scripts pyspark
COPY ./scripts/ ./app/

# User 
USER 1001