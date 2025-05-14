#!/usr/bin/env bash

set -ex

docker run -d --rm \
	--name=agent \
	--publish 2200:22 \
	-e "JENKINS_AGENT_SSH_PUBKEY=$(cat ./.ssh/id_rsa.pub)" \
	jenkins/ssh-agent
