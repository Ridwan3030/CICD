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
                    withEnv(['SONAR_LOGIN=${SONARQUBE_TOKEN}']) {
                        sh """
                        echo Running SonarQube Analysis with CLI...
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
                        sh '''
                        echo "Applying Kubernetes Deployment and Service manifests..."
                        
                        # Apply deployment manifest
                        kubectl apply -f k8s/deployment.yaml

                        # Apply service manifest
                        kubectl apply -f k8s/service.yaml
                        
                        echo "Checking deployment rollout status..."
                        kubectl rollout status deployment/ecom-app
                        
                        echo "Application deployed successfully!"
                        '''
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
