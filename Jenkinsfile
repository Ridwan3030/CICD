pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        AWS_KUBECONFIG = credentials('kubeconfig') // Jenkins credentials for kubeconfig
        FRONTEND_IMAGE = 'your-dockerhub-username/ecom-app-frontend:latest'
        BACKEND_IMAGE = 'your-dockerhub-username/ecom-app-backend:latest'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github', url: 'https://github.com/Kavetec/CICD.git', branch: 'main'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withEnv(['SONAR_LOGIN=${SONARQUBE_TOKEN}']) {
                    sh """
                    echo Running SonarQube Analysis...
                    /opt/sonar-scanner/bin/sonar-scanner \
                      -Dsonar.projectKey=Project-1 \
                      -Dsonar.sources=api,web \
                      -Dsonar.host.url=${SONARQUBE_SERVER_URL} \
                      -Dsonar.login=$SONAR_LOGIN \
                      -Dsonar.inclusions=**/*.py,**/*.html
                    """
                }
            }
        }

        stage('Build Docker Images with Docker Compose') {
            steps {
                script {
                    sh '''
                    echo Logging in to DockerHub...
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin

                    echo Building Docker images...
                    docker compose build
                    '''
                }
            }
        }

        stage('Push Docker Images to DockerHub') {
            steps {
                script {
                    sh '''
                    echo Pushing Docker images...
                    docker compose push
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'kubeconfig']) {
                    script {
                        // Apply the backend deployment and service
                        sh '''
                        kubectl apply -f backend-deployment.yaml
                        kubectl apply -f backend-service.yaml
                        '''
                        
                        // Apply the frontend deployment and service
                        sh '''
                        kubectl apply -f frontend-deployment.yaml
                        kubectl apply -f frontend-service.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed.'
            cleanWs() // Clean up workspace
        }
    }
}
