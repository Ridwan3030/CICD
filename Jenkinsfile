pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SonarQube-Server'                          // Match the server name in Jenkins
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')  // Docker Hub credentials
        GIT_CREDENTIALS = credentials('github')                       // GitHub credentials
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
                    withSonarQubeEnv('SonarQube-Server') {              // Plugin handles authentication
                        sh """
                        sonar-scanner \
                        -Dsonar.projectKey=Project-1 \                  // Project key from SonarQube
                        -Dsonar.sources=api,web \                 // Source directories to analyze
                        -Dsonar.inclusions=**/*.py,**/*.html \
                        -Dsonar.host.url=$SONARQUBE_SERVER             // SonarQube server URL
                        """
                    }
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
