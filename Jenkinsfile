pipeline {
    agent any

    environment {
        IMAGE_NAME = 'aceest-gym-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Setup') {
            steps {
                echo 'Installing Python dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                echo 'Running syntax check...'
                sh 'python -m py_compile app.py'
                echo 'Running flake8 linter...'
                sh 'flake8 app.py tests/ --max-line-length=120 --statistics'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Test') {
            steps {
                echo 'Running Pytest inside Docker container...'
                sh "docker run --rm ${IMAGE_NAME} python -m pytest tests/ -v"
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! All stages passed.'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for details.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
