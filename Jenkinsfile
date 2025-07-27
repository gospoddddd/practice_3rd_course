pipeline {
  agent any

  options {
    timestamps()
    skipDefaultCheckout(true)
  }

  stages {
    stage('Checkout') {
      steps {
        checkout([$class: 'GitSCM',
          branches: [[name: "*/${env.GIT_BRANCH ?: 'main'}"]],
          userRemoteConfigs: [[url: "${env.GIT_REPO_URL ?: 'https://github.com/your-username/practice_3rd_course.git'}"]]
        ])
      }
    }

    stage('Init env') {
      steps {
        script {
          // Значения по умолчанию + возможность переопределить через .env
          env.REGISTRY_FROM_JENKINS = (env.REGISTRY_HOST_FROM_JENKINS?.trim()) ? env.REGISTRY_HOST_FROM_JENKINS : 'host.docker.internal:5000'
          env.REGISTRY_FROM_HOST    = (env.REGISTRY_HOST_FROM_HOST?.trim())    ? env.REGISTRY_HOST_FROM_HOST    : 'localhost:5000'
          env.APP_NAME = 'practice_3rd_course/app'
        }
      }
    }

    stage('Lint & Test in Docker') {
      agent {
        docker {
          image 'python:3.11-slim'
          args  '-v /var/run/docker.sock:/var/run/docker.sock'
          reuseNode true
        }
      }
      steps {
        sh '''
          python -V
          pip install --upgrade pip
          pip install -r app/requirements.txt
          ruff --version || pip install ruff
          black --version || pip install black
          bandit --version || pip install bandit
          ruff check app
          black --check app
          pytest -q
          # GE placeholder — предупреждение, но не проваливаем сборку
          python app/dq/check_ge.py || echo "[WARN] GE placeholder failed or skipped"
        '''
      }
    }

    stage('Build & Push Image') {
      steps {
        script {
          env.IMAGE_TAG = sh(script: "git rev-parse --short=7 HEAD", returnStdout: true).trim()
          sh """
            docker build -t ${env.REGISTRY_FROM_JENKINS}/${env.APP_NAME}:${env.IMAGE_TAG} -f app/Dockerfile .
            docker push ${env.REGISTRY_FROM_JENKINS}/${env.APP_NAME}:${env.IMAGE_TAG}
          """
        }
      }
    }

    stage('Approval') {
      steps {
        timeout(time: 15, unit: 'MINUTES') {
          input message: 'Approve deploy to local PROD?', ok: 'Deploy'
        }
      }
    }

    stage('Deploy to local PROD (docker-compose.prod.yml)') {
      steps {
        sh """
          APP_IMAGE=${env.REGISTRY_FROM_HOST}/${env.APP_NAME}:${env.IMAGE_TAG} docker compose -f docker-compose.prod.yml up -d
        """
      }
    }
  }

  post {
    success {
      script {
        def msg = "✅ ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded. Tag: ${env.IMAGE_TAG}"
        try {
          telegramSend message: msg
        } catch (err) {
          sh """
            curl -s -X POST https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage \
              -d chat_id=${env.TELEGRAM_CHAT_ID} \
              -d text="${msg}"
          """
        }
      }
    }
    failure {
      script {
        def msg = "❌ ${env.JOB_NAME} #${env.BUILD_NUMBER} failed. See: ${env.BUILD_URL}"
        try {
          telegramSend message: msg
        } catch (err) {
          sh """
            curl -s -X POST https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage \
              -d chat_id=${env.TELEGRAM_CHAT_ID} \
              -d text="${msg}"
          """
        }
      }
    }
  }
}
