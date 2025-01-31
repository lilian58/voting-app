pipeline {
    agent any

    environment {
        DOCKER_HUB_USERNAME = 'benng12'
        DOCKER_HUB_PASSWORD = 'passer5..'
        IMAGE_VOTE = 'voting-app-vote'
        IMAGE_RESULT = 'voting-app-result'
        IMAGE_WORKER = 'voting-app-worker'
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
                    // Construire les images Docker
                    docker.build("${IMAGE_VOTE}:latest", './vote')
                    docker.build("${IMAGE_RESULT}:latest", './result')
                    docker.build("${IMAGE_WORKER}:latest", './worker')
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                script {
                    // Se connecter à Docker Hub avec les credentials
                    docker.withRegistry('', 'dockerhub-credentials') {
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
                    // Déployer avec Docker Compose
                    sh 'docker-compose down'  // Arrêter les conteneurs existants
                    sh 'docker-compose up -d'  // Démarrer les nouveaux conteneurs avec les dernières images
                }
            }
        }
    }

    post {
        always {
            cleanWs()  // Nettoyer l'environnement de travail après le pipeline
        }
    }
}
