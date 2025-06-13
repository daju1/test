PROJECT_ROOT=${PWD}

docker run -d \
	--name jkarlos_git_server \
	-p 2220:22 \
	-v ${PROJECT_ROOT}/git-server/keys:/git-server/keys \
	-v ${PROJECT_ROOT}/git-server/repos:/git-server/repos \
	--network jenkins \
	jkarlos/git-server-docker
