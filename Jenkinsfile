@Library('devops@main') _

pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE_VERSION = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                script {
                    repo_checkout(
                        "git@github.com:rohithreddygundreddy/simple-flask-backend.git",
                        "main",
                        "ssh-key"
                    )
                }
            }
        }


        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Security Scan - Bandit') {
            steps {
                bat 'pip install bandit'
                bat 'bandit -r . || true'
            }
        }

        stage('Code Quality - flake8') {
            steps {
                bat 'pip install flake8'
                bat 'flake8 . || true'
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
                bat 'docker build -t backend-app .'
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
                        bat 'docker tag backend-app rohithreddy11/backend-app:latest'
                        bat 'docker push rohithreddy11/backend-app:latest'
                    }
                }
            }
        }

        stage('Run Backend Container') {
            steps {
                script {
                    bat 'docker stop backend-app-container || true'
                    bat 'docker rm backend-app-container || true'
                    bat '''
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
