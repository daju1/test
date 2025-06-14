FROM jenkins/ssh-agent:latest


# Define variables
#ENV GIT_USER=git \
#    GIT_GROUP=git
#ENV GIT_HOME=/home/${GIT_USER}
#ENV SSH_AUTHORIZED_KEYS_FILE=${GIT_HOME}/.ssh/authorized_keys \
#    GIT_REPOSITORIES_PATH=/srv/git

# Create the git user and enable login by assigning a simple password
# Note that BusyBox implementation of `adduser` differs from Debian's
# and therefore options behave slightly differently
#RUN set -eux; \
#    addgroup "${GIT_GROUP}"; \
#    adduser \
#        --gecos "Git User" \
#        --ingroup "${GIT_GROUP}" \
#        --disabled-password \
#        --shell "$(which git-shell)" \
#        "${GIT_USER}" ; \
#    echo "${GIT_USER}:12345" | chpasswd

#ARG USER_NAME
##ARG GROUP_NAME
#ARG USER_ID
#ARG GROUP_ID

#ARG DEBIAN_FRONTEND=noninteractive

# Configure a 'docker' sudo user without password
#RUN apt-get update && apt-get -y install sudo
#RUN addgroup --gid ${GROUP_ID} ${GROUP_NAME}
#RUN adduser --disabled-password --gecos '' --uid ${USER_ID} --gid ${GROUP_ID} ${USER_NAME}
#RUN usermod -aG sudo ${USER_NAME}
#RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers


ARG DOCKER_FULL_TAG
LABEL version=${DOCKER_FULL_TAG}
LABEL description="Ubuntu 18.04 image for docker which will be used by Jenkins"
ENV DOCKER_TAG=${DOCKER_FULL_TAG}

RUN apt-get -qq update && apt-get -qq install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    git-lfs \
    libncursesw5 \
    openjdk-17-jdk \
    python3 \
    time \
    unzip \
    zip

RUN apt-get install -y android-sdk

RUN apt-get -y install mc nano vim

RUN apt-get -y install net-tools iproute2 iputils-ping

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64


# Provide centralized value for Gradle daemon cache otherwise, it will cause HUGE issues with RAM consumption on the server
ENV GRADLE_USER_HOME=/mnt/gradle-cache-rw
RUN mkdir -p ${GRADLE_USER_HOME}
RUN chmod a+w ${GRADLE_USER_HOME}

#######################################################
# Set up scan-host-key script
RUN set -eux
COPY ./scan-host-key.sh /
#######################################################

