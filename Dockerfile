# Build with:
# docker build . --tag <user>/cookie-accept
# Push with:
# docker push <user>/cookie-accept

FROM sitespeedio/browsertime:11.6.3
LABEL maintainer="Cookie Accept Team"

RUN pip3 install selenium

RUN mkdir /opt/cookie-accept
ADD cookie-accept.py /opt/cookie-accept
ADD accept_words.txt /root/
ADD rum-speedindex.js /root/

WORKDIR /root/
ENTRYPOINT ["/opt/cookie-accept/cookie-accept.py", "--chrome_driver", "/usr/src/app/node_modules/@sitespeed.io/chromedriver/vendor/chromedriver", "--headless", "--docker"]
