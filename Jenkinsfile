pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out Employee DevOps Platform...'
                checkout scm
            }
        }

        stage('Docker Check') {
            steps {
                bat 'docker --version'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building backend Docker image...'
                bat 'docker build -t employee-devops-platform-backend:jenkins ./backend'
            }
        }

        stage('Docker Images') {
            steps {
                bat 'docker images employee-devops-platform-backend'
            }
        }
    }
}