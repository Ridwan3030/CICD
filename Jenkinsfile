pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Docker Hub credentials
        GIT_CREDENTIALS = credentials('github')                      // GitHub credentials
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github', url: 'https://github.com/Kavetec/CICD.git', branch: 'main'
            }
        }

        stage('Build Docker Images with Docker Compose') {
            steps {
                script {
                    sh '''
                    echo "Logging in to DockerHub..."
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    
                    echo "Building Docker images using docker-compose..."
                    docker compose build
                    '''
                }
            }
        }

        stage('Push Docker Images with Docker Compose') {
            steps {
                script {
                    sh '''
                    echo "Pushing Docker images to DockerHub..."
                    docker compose push
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
            cleanWs() // Clean up the workspace after the pipeline runs
        }
    }
}
