# https://www.jenkins.io/blog/2023/03/27/repository-signing-keys-changing/

PROJECTS_DIR=$(dirname $(dirname ${PWD}))
USR3_DIR=$(dirname $(dirname $(dirname $(dirname ${PWD}))))

docker run \
  --name jenkins-blueocean \
  --restart=on-failure \
  --detach \
  --network jenkins \
  --env DOCKER_HOST=tcp://docker:2376 \
  --env DOCKER_CERT_PATH=/certs/client \
  --env DOCKER_TLS_VERIFY=1 \
  --publish 8080:8080 \
  --publish 50000:50000 \
  --volume ${PROJECTS_DIR}:${PROJECTS_DIR} \
  --volume ${USR3_DIR}/CI_CD:${USR3_DIR}/CI_CD \
  --volume /home/${USER}/jenkins:/home/${USER}/jenkins \
  --volume jenkins-data:/var/jenkins_home \
  --volume jenkins-docker-certs:/certs/client:ro \
  myjenkins-blueocean:2.492.3-1
