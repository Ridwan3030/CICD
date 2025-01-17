pipeline {
    agent any

    environment {
        SONARQUBE_SERVER_URL = 'http://18.212.232.24:9000/'       // Replace with your SonarQube server URL
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
                    withEnv(['SONAR_LOGIN=${SONARQUBE_TOKEN}']) {
                        sh """
                        echo Running SonarQube Analysis with CLI...
                        /opt/sonar-scanner/bin/sonar-scanner \
                          -Dsonar.projectKey=Project-2 \
                          -Dsonar.sources=api,web \
                          -Dsonar.host.url=${SONARQUBE_SERVER_URL} \
                          -Dsonar.login=$SONAR_LOGIN \
                          -Dsonar.inclusions=**/*.py,**/*.html
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

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        // Apply the backend deployment and service
                        sh '''
                        echo "Applying backend deployment and service..."
                        kubectl apply -f backend-deployment.yaml
                        kubectl apply -f backend-service.yaml
                        '''

                        // Apply the frontend deployment and service
                        sh '''
                        echo "Applying frontend deployment and service..."
                        kubectl apply -f frontend-deployment.yaml
                        kubectl apply -f frontend-service.yaml
                        '''

                        echo "Checking backend deployment rollout status..."
                        sh 'kubectl rollout status deployment/backend'

                        echo "Checking frontend deployment rollout status..."
                        sh 'kubectl rollout status deployment/frontend'

                        echo "Application deployed successfully!"
                    }
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
