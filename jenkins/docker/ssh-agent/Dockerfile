#FROM jenkins/ssh-agent:latest
FROM jenkins/ssh-agent:jdk11

RUN apt-get -y install git mc nano vim

RUN apt-get -y install net-tools iproute2 iputils-ping

#######################################################
# Set up scan-host-key script
RUN set -eux
COPY ./scan-host-key.sh /
#######################################################

COPY ./setup-sshd /usr/local/bin/