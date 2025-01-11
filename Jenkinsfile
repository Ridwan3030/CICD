pipeline {
    agent any

    environment {
        SONARQUBE_SERVER_URL = 'http://54.237.203.34:9000/'       // Replace with your SonarQube server URL
        SONARQUBE_TOKEN = credentials('SonarQube-Server')               // SonarQube authentication token from Jenkins credentials
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')   // Docker Hub credentials
        GIT_CREDENTIALS = credentials('github')                        // GitHub credentials
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github', url: 'https://github.com/Kavetec/CICD.git', branch: 'main'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    sh """
                    echo "Running SonarQube Analysis with CLI..."
                    sonar-scanner \
                        -Dsonar.projectKey=Project-1 \
                        -Dsonar.sources=api,web \
                        -Dsonar.host.url=${SONARQUBE_SERVER_URL} \
                        -Dsonar.login=${SONARQUBE_TOKEN} \
                        -Dsonar.inclusions=**/*.py,**/*.html
                    """
                }
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
