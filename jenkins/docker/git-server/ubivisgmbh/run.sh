PROJECT_ROOT=$(dirname ${PWD})

docker run -d -p 2022:22 \
	--name ubivisgmbh_git_server \
	-v ${PROJECT_ROOT}/gitserver:/srv/git \
 	-e GIT_AUTHORIZED_KEYS="$(cat ~/.ssh/id_rsa.pub)" \
	-e GIT_HOST_HINT="example.org:2022" \
	--network jenkins \
	ubivisgmbh/git-server
