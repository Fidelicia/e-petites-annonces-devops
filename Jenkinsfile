pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t app-devops -f docker/Dockerfile .'
            }
        }
        stage('Test') {
            steps {
                sh 'docker rm -f test-container || true'
                sh 'docker run -d --name test-container -p 8082:80 app-devops'
                sh 'sleep 8'
                sh 'docker exec test-container curl -f http://localhost:80/ || exit 1'
                sh 'docker stop test-container'
                sh 'docker rm test-container'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker stop app-devops-prod || true'
                sh 'docker rm app-devops-prod || true'
                sh 'docker network create reseau-devops || true'
                sh 'docker run -d --name app-devops-prod --network reseau-devops -p 8080:80 app-devops'
            }
        }
    }

    post {
        success {
            echo 'Pipeline terminé avec succès : application déployée.'
        }
        failure {
            echo 'Le pipeline a échoué.'
        }
    }
}
