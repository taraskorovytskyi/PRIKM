pipeline {
    agent any

    environment {
        DOCKERHUB_USER = "tarasitpa"
        IMAGE_NAME = "${DOCKERHUB_USER}/prikm"
    }

    stages {
        stage('Start') {
            steps {
                echo 'Lab_2: started by GitHub'
            }
        }

        stage('Image build') {
            steps {
                sh "docker build -t prikm:latest ."
                sh "docker tag prikm ${IMAGE_NAME}:latest"
                sh "docker tag prikm ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Push to registry') {
            steps {
                withDockerRegistry([ credentialsId: "dockerhub_token", url: "" ]) {
                    sh "docker push ${IMAGE_NAME}:latest"
                    sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }

        stage('Deploy image') {
            steps {
                sh '''
                    echo "[INFO] Cleaning port 80..."
                    containers=$(docker ps --filter "publish=80" --format "{{.ID}}")
                    if [ -n "$containers" ]; then
                        echo "[INFO] Stopping containers on port 80..."
                        docker stop $containers
                        echo "[INFO] Removing containers on port 80..."
                        docker rm $containers
                    fi

                    echo "[INFO] Running new container on port 80..."
                    docker run -d -p 80:80 ${IMAGE_NAME}
                '''
            }
        }
    }
}
