# Build with:
# docker build . --tag <user>/priv-accept
# Push with:
# docker push <user>/priv-accept

FROM sitespeedio/browsertime:11.6.3
LABEL maintainer="Priv Accept Team"

RUN pip3 install selenium pyvirtualdisplay

RUN mkdir /opt/priv-accept
ADD priv-accept.py /opt/priv-accept
ADD accept_words.txt /root/
ADD rum-speedindex.js /root/

WORKDIR /root/
ENTRYPOINT ["/opt/priv-accept/priv-accept.py", "--chrome_driver", "/usr/src/app/node_modules/@sitespeed.io/chromedriver/vendor/chromedriver", "--docker"]
