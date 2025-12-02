pipeline {
  agent { label 'ansible-agent' }
  environment {
    REPO = "https://github.com/slendchat/ticket-system-demo.git"
  }
  stages {
    stage('Checkout app') {
      steps {
        git url: "${env.REPO}"
      }
    }

    stage('Prepare Ansible deploy') {
      steps {
        // Подготовить inventory/vars или воспользоваться существующим playbook'ом
        sh '''
          # создаём временную папку с проектом для копирования
          mkdir -p /tmp/deploy_project
          rsync -a --delete . /tmp/deploy_project/
        '''
      }
    }

    stage('Deploy via Ansible') {
      steps {
        // используем ansible copy/rsync или playbook, который копирует /tmp/deploy_project -> /var/www/project
        sh '''
          if [ -n "$ANSIBLE_PRIVATE_KEY" ]; then
            echo "$ANSIBLE_PRIVATE_KEY" > /home/ansible/.ssh/ansible_to_testserver_key
            chmod 600 /home/ansible/.ssh/ansible_to_testserver_key
          fi

          ansible -i ansible/hosts.ini testserver -m copy -a "src=/tmp/deploy_project/ dest=/var/www/project owner=www-data group=www-data mode=0755" --private-key=/home/ansible/.ssh/ansible_to_testserver_key -u ansible
          # перезапустить apache если нужно
          ansible -i ansible/hosts.ini testserver -m service -a "name=apache2 state=restarted" --private-key=/home/ansible/.ssh/ansible_to_testserver_key -u ansible
        '''
      }
    }
  }
  post {
    always { cleanWs() }
  }
}
