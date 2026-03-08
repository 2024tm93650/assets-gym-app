pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/2024tm93650/assets-gym-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                sh 'python -m py_compile app.py'
                sh 'flake8 app.py tests/ --max-line-length=120'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t aceest-gym-app .'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'docker run --rm aceest-gym-app python -m pytest tests/ -v'
            }
        }
    }
}