pipeline {
    agent {
        label 'php-agent'
    }
    
    stages {        
        stage('Клонирование репозитория') {
            steps {
                echo 'Клонирование PHP проекта...'
                git 'https://github.com/slendchat/ticket-system-demo.git'
            }
        }
        
        stage('Установка зависимостей') {
            steps {
                echo 'Установка зависимостей Composer...'
                sh 'composer install --no-dev --optimize-autoloader'
            }
        }
        
        stage('Тестирование') {
            steps {
                echo 'Запуск PHPUnit тестов...'
                sh 'vendor/bin/phpunit --testdox'
            }
        }
        
        stage('Статический анализ') {
            steps {
                echo 'Запуск PHPStan...'
                sh 'vendor/bin/phpstan analyse'
            }
        }
    }
    
    post {
        always {
            echo 'Пайплайн завершен.'
            cleanWs()
        }
        success {
            echo 'Все этапы выполнены успешно! ✅'
        }
        failure {
            echo 'Обнаружены ошибки в пайплайне! ❌'
        }
    }
}