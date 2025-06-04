pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub_token'
        DOCKERHUB_USER = 'tarasitpa'
        IMAGE_NAME = 'prikm'
        IMAGE_TAG = "${BUILD_NUMBER}"
        WEBHOOK_URL = credentials('teams_webhook_url') // з Jenkins credentials
    }

    stages {
        stage('Start') {
            steps {
                echo 'Start Lab_7 + Lab_2'
            }
        }

        stage('Auth to HCP') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'hcp',
                    usernameVariable: 'MY_ID', passwordVariable: 'MY_SECRET')]) {
                    script {
                        sh 'hcp auth login --client-id $MY_ID --client-secret $MY_SECRET'
                    }
                }
            }
        }

        stage('Init HCP Profile') {
            steps {
                sh 'hcp profile set vault-secrets/app lab-7'
            }
        }

        stage('Image build') {
            steps {
                sh """
                    docker build -t ${IMAGE_NAME}:latest .
                    docker tag ${IMAGE_NAME}:latest ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                    docker tag ${IMAGE_NAME}:latest ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withDockerRegistry([ credentialsId: "${DOCKERHUB_CREDENTIALS}", url: "https://index.docker.io/v1/" ]) {
                    sh """
                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                        docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                    """
                }
            }
        }

        stage('Deploy image') {
            steps {
                sh """
                    echo "[INFO] Cleaning port 80..."
                    containers=\$(docker ps --filter publish=80 --format {{.ID}})
                    if [ -n "\$containers" ]; then
                        docker stop \$containers
                        docker rm \$containers
                    fi

                    docker run -d -p 80:80 ${DOCKERHUB_USER}/${IMAGE_NAME}
                """
            }
        }

        stage('Send Teams notification') {
            steps {
                office365ConnectorSend message: "✅ Deploy успішний! Tag: ${IMAGE_TAG}",
                                       webhookUrl: "${WEBHOOK_URL}"
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished (success/failure)'
        }
        failure {
            office365ConnectorSend message: "❌ Pipeline завершився з помилкою. Перевір Jenkins лог!",
                                   webhookUrl: "${WEBHOOK_URL}"
        }
    }
}
