docker build \
    --build-arg USER_NAME=${USER} \
    --build-arg GROUP_NAME=${USER} \
    --build-arg USER_ID=$(id -u ${USER}) \
    --build-arg GROUP_ID=$(id -g ${USER}) \
    -t myjenkins-blueocean:2.492.3-1 .
