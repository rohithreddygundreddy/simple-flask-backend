@Library('devops@main') _

pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                script {
                    repo_checkout()
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Security Scan - Bandit') {
            steps {
                sh 'pip install bandit'
                sh 'bandit -r . || true'
            }
        }

        stage('Code Quality - flake8') {
            steps {
                sh 'pip install flake8'
                sh 'flake8 . || true'
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    build()   // from your shared library
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t backend-app .'
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
                        sh 'docker tag backend-app rohithreddy11/backend-app:latest'
                        sh 'docker push rohithreddy11/backend-app:latest'
                    }
                }
            }
        }

        stage('Run Backend Container') {
            steps {
                script {
                    sh 'docker stop backend-app-container || true'
                    sh 'docker rm backend-app-container || true'
                    sh '''
                        docker run -d \
                        --name backend-app-container \
                        -p 5000:5000 \
                        rohithreddy11/backend-app:latest
                    '''
                }
            }
        }
    }
}
