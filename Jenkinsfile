pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Docker Hub credentials
        GIT_CREDENTIALS = credentials('github')                      // GitHub credentials
        IMAGE_NAME = 'isaackavetec/cicd'                            // Replace with your Docker Hub repo name
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github', url: 'https://github.com/yourusername/ecom-app.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh '''
                    docker build -t $IMAGE_NAME:latest .
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
        }
    }
}
