@Library('devops@main') _

pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        PYTHON = "C:\\Users\\srija\\AppData\\Local\\Programs\\Python\\Python314\\python.exe"
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
                    "%PYTHON%" -m pip install -r requirements.txt
                """
            }
        }

        stage('Security Scan - Bandit') {
            steps {
                bat """
                    "%PYTHON%" -m pip install bandit

                    rem Run Bandit but NEVER fail the pipeline
                    cmd /c ""%PYTHON%" -m bandit -r . & exit /b 0"
                """
            }
        }


        stage('Code Quality - flake8') {
            steps {
                bat """
                    "%PYTHON%" -m pip install flake8
                    "%PYTHON%" -m flake8 . || echo flake8 warnings found
                """
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    build()   // from shared library (uses full Python path)
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
                    docker stop backend-app-container || echo No container
                    docker rm backend-app-container || echo No container

                    docker run -d --name backend-app-container -p 5000:5000 rohithreddy11/backend-app:%IMAGE_VERSION%
                """
            }
        }
    }
}
