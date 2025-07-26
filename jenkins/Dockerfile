FROM jenkins/jenkins:lts-jdk17

USER root

# Basic tools and Docker CLI to talk to host Docker via mounted /var/run/docker.sock
RUN apt-get update &&     apt-get install -y --no-install-recommends docker.io git curl jq &&     rm -rf /var/lib/apt/lists/*

USER jenkins

# Pre-install plugins (latest compatible versions)
# Note: telegram-notifications is old; installed for demo usage as requested.
RUN jenkins-plugin-cli --plugins   configuration-as-code   credentials-binding   job-dsl   git   workflow-aggregator   pipeline-stage-view   docker-workflow   pipeline-utility-steps   blueocean   telegram-notifications
