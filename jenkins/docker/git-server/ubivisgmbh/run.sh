USR3_ROOT=$(dirname $(dirname $(dirname $(dirname $(dirname ${PWD})))))
PROJECT_ROOT=$(dirname$(dirname ${PWD}))

docker run -d -p 2022:22 \
	--name ubivisgmbh_git_server \
	-v ${USR3_ROOT}/CI_CD/gitserver:/srv/git \
 	-e GIT_AUTHORIZED_KEYS="$(cat ~/.ssh/id_rsa.pub)" \
	-e GIT_HOST_HINT="example.org:2022" \
	--network jenkins \
	ubivisgmbh/git-server
