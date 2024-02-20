# Build with:
# docker build . --tag <user>/priv-accept
# Push with:
# docker push <user>/priv-accept
# Use an official Python runtime as a parent image
FROM python:3.8
LABEL maintainer="Priv Accept"

# Set the working directory in the container
WORKDIR /root/
USER root

# install xvfb to enable no-headless (headful) mode
RUN apt update && apt install -y python3-pip xvfb && apt upgrade -y
ENV DISPLAY=:0

# install chrome version: 114
ENV CHROME_VERSION=114.0.5735.198-1
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb
RUN apt-get -y update
RUN apt-get install -y ./google-chrome-stable_${CHROME_VERSION}_amd64.deb

# install chromedriver: 2/20/2024: version is 114
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Copy the current directory contents into the container
RUN mkdir /opt/priv-accept
ADD priv-accept.py /opt/priv-accept
ADD accept_words.txt /root/
ADD urls.txt /root/
ADD rum-speedindex.js /root/
ADD parse.py /root/
ADD run_priv.sh /opt/priv-accept

RUN pip install selenium pandas


# Make port 80 available to the world outside this container
EXPOSE 80


# Run run_priv.sh when the container launches
CMD xvfb-run --server-args="-screen 0 1900x1200x24" /opt/priv-accept/run_priv.sh urls.txt

# Run priv-accept and follow with the output.csv parse.py
# CMD xvfb-run --server-args="-screen 0 1900x1200x24" /opt/priv-accept/run_priv.sh urls.txt && python ./parse.py