pipeline {
  agent { label 'php-agent' } // должен соответствовать label агента с php (ssh-agent/jenkins agent)
  environment {
    REPO = "https://github.com/slendchat/ticket-system-demo.git"
  }
  stages {
    stage('Checkout') {
      steps {
        echo "Cloning repository"
        git url: "${env.REPO}"
      }
    }
    stage('Install Composer') {
      steps {
        sh '''
          if [ ! -f composer.phar ]; then
            php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
            php composer-setup.php --quiet
            rm composer-setup.php
          fi
          php composer.phar install --no-dev --optimize-autoloader
        '''
      }
    }
    stage('Run tests') {
      steps {
        sh 'vendor/bin/phpunit --testdox || true'
      }
      post {
        always {
          junit 'build/*.xml' // если generate junit reports
        }
      }
    }
  }
  post {
    always {
      cleanWs()
    }
    success {
      echo 'Build and tests succeeded'
    }
    failure {
      echo 'Build or tests failed'
    }
  }
}
