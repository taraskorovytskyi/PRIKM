pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub_token' // ID облікових даних в Jenkins
        DOCKERHUB_USER = 'tarasitpa'
        IMAGE_NAME = 'prikm'
        IMAGE_TAG = "${BUILD_NUMBER}"
        TEAMS_WEBHOOK = 'https://lpnu.webhook.office.com/webhookb2/dc0a6495-7ea0-443e-b2c5-a740df974e31@7631cd62-5187-4e15-8b8e-ef653e366e7a/IncomingWebhook/8689910739e7460cb8b7c0eeae135013/c3f18ca5-a7b5-4a8b-836b-815b3ad365d5/V2QVHrqnohHfmyOlPNVeRDiV9qB_B2j5EWPUZhk4J3Vhc1'
    }

    stages {
        stage('Start') {
            steps {
                echo 'Lab_2: started by GitHub'
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

        stage('Push to registry') {
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
                        echo "[INFO] Stopping containers on port 80..."
                        docker stop \$containers
                        echo "[INFO] Removing containers on port 80..."
                        docker rm \$containers
                    fi

                    echo "[INFO] Running new container on port 80..."
                    docker run -d -p 80:80 ${DOCKERHUB_USER}/${IMAGE_NAME}
                """
            }
        }

        stage('Send Teams notification') {
            steps {
                office365ConnectorSend message: "✅ Deploy успішний! Tag: ${IMAGE_TAG}",
                                       webhookUrl: "${TEAMS_WEBHOOK}"
            }
        }
    }

    post {
        failure {
            office365ConnectorSend message: "❌ Deploy провалився. Перевір Jenkins лог.",
                                   webhookUrl: "${TEAMS_WEBHOOK}"
        }
    }
}
