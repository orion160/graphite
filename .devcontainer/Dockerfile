FROM python:latest

RUN apt update && apt upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt install -y \
        sudo git wget lsb-release locales \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && groupadd devgroup \
    && useradd -g devgroup -m -s /bin/bash dev \
    && echo "dev ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    && echo "LANG=en_US.utf8" >> /etc/environment \

USER dev

WORKDIR /workspace
