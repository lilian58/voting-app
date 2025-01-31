pipeline { 
    agent any

    environment {
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
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', 
                                                     usernameVariable: 'benng12', 
                                                     passwordVariable: 'Avoir2profil#Dev#Sec.')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    }
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    sh "docker push ${IMAGE_VOTE}:latest"
                    sh "docker push ${IMAGE_RESULT}:latest"
                    sh "docker push ${IMAGE_WORKER}:latest"
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
