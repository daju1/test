#!/bin/sh
#
host_ip=$1

ssh-keyscan -H ${host_ip} >> /root/.ssh/known_hosts
ssh-keyscan ${host_ip} >> /var/jenkins_home/.ssh/known_hosts