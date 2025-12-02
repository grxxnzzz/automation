pipeline {
  agent { label 'ansible-agent' }
  environment {
    PLAYBOOK_REPO = "https://github.com/yourusername/yourrepo.git" // репо где лежит ansible/
  }
  stages {
    stage('Checkout playbook') {
      steps {
        git url: "${env.PLAYBOOK_REPO}"
      }
    }
    stage('Prepare SSH key') {
      steps {
        // Предполагается, что в Jenkins credentials есть SSH Private Key с ID 'ansible-to-testserver-key'
        // Этот шаг сохранит ключ в нужное место внутри рабочей ноды.
        sshagent (credentials: ['ansible-to-testserver-key']) {
          sh '''
            mkdir -p /home/ansible/.ssh
            # sshagent plugin подставит приватный ключ в ssh-agent; также скопируем его файл если нужно
            # Но удобнее: используйте credentials binding или writeFile в Jenkins
          '''
        }
      }
    }
    stage('Run Ansible Playbook') {
      steps {
        sh '''
          # Записываем приватный ключ в файл (credential must be injected via Jenkins credential binding)
          if [ -n "$ANSIBLE_PRIVATE_KEY" ]; then
            echo "$ANSIBLE_PRIVATE_KEY" > /home/ansible/.ssh/ansible_to_testserver_key
            chmod 600 /home/ansible/.ssh/ansible_to_testserver_key
          fi
          ansible-playbook -i ansible/hosts.ini ansible/setup_test_server.yml --private-key=/home/ansible/.ssh/ansible_to_testserver_key -u ansible -k
        '''
      }
    }
  }
  post {
    always {
      cleanWs()
    }
  }
}
