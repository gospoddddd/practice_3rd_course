FROM jenkins/jenkins:lts-jdk17

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends docker.io git curl jq && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

# Задаём зеркала Jenkins (уменьшает вероятность обрыва скачивания)
ARG JENKINS_UC=https://updates.jenkins.io
ARG JENKINS_UC_DOWNLOAD=https://mirror.jenkins-ci.org
ENV JENKINS_UC=${JENKINS_UC} \
    JENKINS_UC_DOWNLOAD=${JENKINS_UC_DOWNLOAD}

# Минимальный набор плагинов, достаточный для нашего пайплайна
# (Blue Ocean и Stage View исключил — они тянут длинные цепочки зависимостей и часто ломаются на сетях)
RUN jenkins-plugin-cli --plugins \
  configuration-as-code \
  credentials-binding \
  job-dsl \
  git \
  workflow-aggregator \
  docker-workflow \
  pipeline-utility-steps \
  telegram-notifications
