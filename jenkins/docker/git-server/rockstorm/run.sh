USR3_ROOT=$(dirname $(dirname $(dirname $(dirname $(dirname ${PWD})))))
PROJECT_ROOT=$(dirname$(dirname ${PWD}))

docker run -d -p 2202:22 \
	--name rockstorm_git_server \
	-v ${USR3_ROOT}/CI_CD/gitserver:/srv/git \
	-v ${PROJECT_ROOT}/ssh-agent/.ssh/id_rsa.pub:/home/git/.ssh/authorized_keys \
	--network jenkins \
	--env SSH_AUTH_METHODS=publickey \
	rockstorm/git-server