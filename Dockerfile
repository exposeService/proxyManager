ARG ARCH=
ARG GOLANG_VERSION=1.20
ARG ALPINE_VERSION=3.18

FROM ${ARCH}golang:${GOLANG_VERSION}-alpine${ALPINE_VERSION} as builder

ARG wg_go_tag=0.0.20230223
ARG wg_tools_tag=v1.0.20210914

RUN apk add --update git build-base libmnl-dev iptables

RUN git clone https://git.zx2c4.com/wireguard-go && \
    cd wireguard-go && \
    git checkout $wg_go_tag && \
    make && \
    make install

ENV WITH_WGQUICK=yes
RUN git clone https://git.zx2c4.com/wireguard-tools && \
    cd wireguard-tools && \
    git checkout $wg_tools_tag && \
    cd src && \
    make && \
    make install

FROM python:3.9.10-alpine

COPY --from=builder /usr/bin/wireguard-go /usr/bin/wg* /usr/bin/

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt ./

RUN apk add wireguard-tools-wg-quick
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

COPY ./app .
CMD ["python3", "app.py"]

