properties([
    pipelineTriggers([]),
    office365ConnectorWebhooks([
        [
            name: 'Lab_3',
            url: 'https://lpnu.webhook.office.com/webhookb2/dc0a6495-7ea0-443e-b2c5-a740df974e31@7631cd62-5187-4e15-8b8e-ef653e366e7a/IncomingWebhook/8689910739e7460cb8b7c0eeae135013/c3f18ca5-a7b5-4a8b-836b-815b3ad365d5/V2QVHrqnohHfmyOlPNVeRDiV9qB_B2j5EWPUZhk4J3Vhc1',
            startNotification: false,
            notifySuccess: true,
            notifyAborted: false,
            notifyNotBuilt: false,
            notifyUnstable: true,
            notifyFailure: true,
            notifyBackToNormal: true,
            notifyRepeatedFailure: false,
            timeout: 30000
        ]
    ])
])

pipeline {
    agent any

    environment {
        CONTAINER_NAME = "prikm_lab3"
        IMAGE_NAME = "squeezyfish/prikm"
    }

    stages {
        stage('Start') {
            steps {
                echo 'Lab_3: started by GitHub'
            }
        }

        stage('Cleanup old containers') {
            steps {
                sh '''
                    if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
                        echo "Stopping and removing existing container: $CONTAINER_NAME"
                        docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME
                    else
                        echo "No existing container found, skipping cleanup."
                    fi
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t prikm:latest .
                    docker tag prikm $IMAGE_NAME:latest
                    docker tag prikm $IMAGE_NAME:$BUILD_NUMBER
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                withDockerRegistry([credentialsId: "dockerhub_token", url: ""]) {
                    sh '''
                        docker push $IMAGE_NAME:latest
                        docker push $IMAGE_NAME:$BUILD_NUMBER
                    '''
                }
            }
        }

        stage('Deploy Image') {
            steps {
                sh '''
                    docker run -d --name $CONTAINER_NAME -p 80:80 $IMAGE_NAME:latest
                    echo "✅ Deployment completed!"
                '''
            }
        }
    }

    post {
        success {
            office365ConnectorSend message: "✅ Lab3: Build & Deploy успішні! Tag: latest", webhookName: 'Lab_3'
        }
        failure {
            office365ConnectorSend message: "❌ Lab3: Build не вдалося. Перевір логи Jenkins!", webhookName: 'Lab_3'
        }
    }
}

