#!/bin/sh
#
host_ip=$1

ssh-keyscan ${host_ip} >> /home/jenkins/.ssh/known_hosts