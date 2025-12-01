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
                bat """
                    pip install -r requirements.txt
                """
            }
        }

        stage('Security Scan - Bandit') {
            steps {
                bat """
                    pip install bandit
                    bandit -r . || echo "Bandit scan completed with warnings"
                """
            }
        }

        stage('Code Quality - flake8') {
            steps {
                bat """
                    pip install flake8
                    flake8 . || echo "Flake8 warnings found"
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    build()    // Your shared library build.groovy
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat """
                    docker build -t backend-app:%IMAGE_VERSION% .
                    docker tag backend-app:%IMAGE_VERSION% backend-app:latest
                """
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                bat """
                    docker tag backend-app:%IMAGE_VERSION% rohithreddy11/backend-app:%IMAGE_VERSION%
                    docker push rohithreddy11/backend-app:%IMAGE_VERSION%

                    docker tag backend-app:%IMAGE_VERSION% rohithreddy11/backend-app:latest
                    docker push rohithreddy11/backend-app:latest
                """
            }
        }

        stage('Run Backend Container') {
            steps {
                bat """
                    docker stop backend-app-container || echo "No running container"
                    docker rm backend-app-container || echo "No container to remove"

                    docker run -d --name backend-app-container -p 5000:5000 rohithreddy11/backend-app:%IMAGE_VERSION%
                """
            }
        }
    }
}
