# https://www.jenkins.io/blog/2023/03/27/repository-signing-keys-changing/
# https://pkg.origin.jenkins.io/debian-stable/
# https://www.jenkins.io/doc/book/installing/docker/

FROM jenkins/jenkins:2.492.3-jdk17


ARG USER_NAME
ARG GROUP_NAME
ARG USER_ID
ARG GROUP_ID

ARG DEBIAN_FRONTEND=noninteractive

# Configure a 'docker' sudo user without password
RUN apt-get update && apt-get -y install sudo
RUN addgroup --gid ${GROUP_ID} ${GROUP_NAME}
RUN adduser --disabled-password --gecos '' --uid ${USER_ID} --gid ${GROUP_ID} ${USER_NAME}
RUN usermod -aG sudo ${USER_NAME}
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Customize the official Jenkins Docker image, by executing the following two steps:
USER root
RUN apt-get update && apt-get install -y lsb-release ca-certificates curl && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
    https://download.docker.com/linux/debian $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && apt-get install -y docker-ce-cli && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

#######################################################
# Ghemical
# Install build-essential package (for cross compilation)
RUN apt-get update
RUN apt-get -y install build-essential

# Install vim, nano
RUN apt-get -y install vim nano

# Install a bunch of packages for project

RUN apt-get -y install git

#######################################################

USER jenkins
RUN jenkins-plugin-cli --plugins "blueocean docker-workflow"
