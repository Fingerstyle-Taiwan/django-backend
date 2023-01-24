pipeline {
    agent any 
    stages {
        stage('Build') { 
            steps {
                echo 'Start Building...'
                sh 'docker-compose build'
            }
        }
        stage('Test') { 
            steps {
                echo 'Start Testing...'
                sh 'docker-compose run --rm django-app sh -c "python manage.py test"'
            }
        }
        stage('Lint') { 
            steps {
                echo 'Start Lint Checking...'
                sh 'docker-compose run --rm django-app sh -c "black . && isort . && flake8"'
            }
        }
    }
}