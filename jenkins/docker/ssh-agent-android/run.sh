#!/usr/bin/env bash

set -ex

docker run -d --rm \
	--name=agent_android \
	--publish 2222:22 \
	-e "JENKINS_AGENT_SSH_PUBKEY=$(cat ./.ssh/id_rsa.pub)" \
	--network jenkins \
	ssh-agent-android:latest
