pipeline {
    agent any

    environment {
        DOCKER_HUB_USERNAME = 'benng12'
        DOCKER_HUB_PASSWORD = 'passer5..'
        IMAGE_VOTE = 'benng12/voting-app-vote'
        IMAGE_RESULT = 'benng12/voting-app-result'
        IMAGE_WORKER = 'benng12/voting-app-worker'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/lilian58/voting-app.git'
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    docker.build("${IMAGE_VOTE}:latest", './vote')
                    docker.build("${IMAGE_RESULT}:latest", './result')
                    docker.build("${IMAGE_WORKER}:latest", './worker')
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'dockerhub-credentials') {
                        docker.image("${IMAGE_VOTE}:latest").push()
                        docker.image("${IMAGE_RESULT}:latest").push()
                        docker.image("${IMAGE_WORKER}:latest").push()
                    }
                }
            }
        }

        stage('Deploy to Docker Compose') {
            steps {
                script {
                    sh 'docker-compose -f ./docker-compose.yml down'
                    sh 'docker-compose -f ./docker-compose.yml up -d'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
