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
                sh '''
                    TEST_IP=$(docker inspect -f "{{.NetworkSettings.IPAddress}}" test-container)
                    echo "IP du conteneur de test : $TEST_IP"
                    for i in $(seq 1 15); do
                        if curl -sf http://$TEST_IP:80/ > /dev/null; then
                            echo "Application disponible (tentative $i)"
                            exit 0
                        fi
                        echo "Tentative $i : pas encore prete, attente 3s..."
                        sleep 3
                    done
                    echo "Echec : application non disponible apres 45s"
                    docker logs test-container
                    exit 1
                '''
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
