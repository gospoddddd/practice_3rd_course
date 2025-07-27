FROM jenkins/jenkins:lts-jdk17

USER root

# Базовые утилиты + Docker CLI + docker compose plugin
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      docker.io \
      docker-compose-plugin \
      git \
      curl \
      jq && \
    # добавить пользователя jenkins в группу docker (для доступа к /var/run/docker.sock)
    usermod -aG docker jenkins && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

# Плагины Jenkins (минимум, без Blue Ocean/Stage View)
ARG JENKINS_UC=https://updates.jenkins.io
ARG JENKINS_UC_DOWNLOAD=https://mirror.jenkins-ci.org
ENV JENKINS_UC=${JENKINS_UC} JENKINS_UC_DOWNLOAD=${JENKINS_UC_DOWNLOAD}

RUN jenkins-plugin-cli --plugins \
  configuration-as-code \
  credentials-binding \
  job-dsl \
  git \
  workflow-aggregator \
  docker-workflow \
  pipeline-utility-steps \
  telegram-notifications
