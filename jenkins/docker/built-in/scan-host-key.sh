#!/bin/sh
#
host_ip=$1
workdir=$2

ssh-keyscan -H ${host_ip} >> ${workdir}/.ssh/known_hosts
