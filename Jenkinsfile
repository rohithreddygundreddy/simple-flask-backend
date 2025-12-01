@Library('devops@main') _

pipeline {
    agent any

    options { skipDefaultCheckout(true) }

    environment {
        PYTHON = "C:\\Users\\srija\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"
        IMAGE_VERSION = "${BUILD_NUMBER}"
        DOCKERHUB_USER = "rohithreddy11"
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
                    "%PYTHON%" -m pip install -r requirements.txt
                """
            }
        }

        stage('Security Scan - Bandit') {
            steps {
                bat """
                    "%PYTHON%" -m pip install bandit
                    cmd /c ""%PYTHON%" -m bandit -r . & exit /b 0"
                """
            }
        }

        stage('Code Quality - flake8') {
            steps {
                bat """
                    "%PYTHON%" -m pip install flake8
                    cmd /c ""%PYTHON%" -m flake8 . & exit /b 0"
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    build()
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
                    docker tag backend-app:%IMAGE_VERSION% %DOCKERHUB_USER%/backend-app:%IMAGE_VERSION%
                    docker push %DOCKERHUB_USER%/backend-app:%IMAGE_VERSION%

                    docker tag backend-app:%IMAGE_VERSION% %DOCKERHUB_USER%/backend-app:latest
                    docker push %DOCKERHUB_USER%/backend-app:latest
                """
            }
        }

        stage('Run Backend Container') {
            steps {
                bat """
                    docker stop backend-app-container || echo No container
                    docker rm backend-app-container || echo No container

                    docker run -d --name backend-app-container -p 5000:5000 %DOCKERHUB_USER%/backend-app:%IMAGE_VERSION%
                """
            }
        }
    }
}
