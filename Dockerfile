FROM docker.1ms.run/library/python:3.13-alpine3.23
RUN mkdir -p /opt/
WORKDIR /opt/
COPY . .
RUN pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple && \
    pip3 install -r requirements.txt --no-cache-dir && \
    chmod +x start.sh
EXPOSE 8000
CMD ["bash","start.sh"]