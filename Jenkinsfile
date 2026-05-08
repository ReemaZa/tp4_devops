pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = tool 'SonarScanner'
        DOCKER_HUB_USER = "riza239" 
        IMAGE_NAME = "app-flask-tp4"
        REGISTRY_CREDS = "dockerhub-creds" 
    }

    stages {
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt --break-system-packages'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m pytest test_app.py'
            }
        }

        stage('Static Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') { 
                    sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=Flask_App_TP4 \
                    -Dsonar.sources=. \
                    -Dsonar.language=py"
                }
            }
        }

        stage("Quality Gate") {
            steps {
                waitForQualityGate abortPipeline: true
            }
        }

        stage('Docker Build') {
            steps {
                // Utilisation de doubles quotes pour permettre l'interpolation des variables
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        stage('Image Scanning (Trivy)') {
            steps {
                // Scan de l'image construite
                sh "trivy image --severity HIGH,CRITICAL ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDS}", usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
                }
            }
        }
        stage('Infrastructure Provisioning (Terraform)') {
            steps {
                dir('terraform') {
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Deploy App (Ansible)') {
            steps {
                // On s'assure que la collection K8s est là
                sh 'ansible-galaxy collection install kubernetes.core'
                
                dir('ansible') {
                    // C'est ici qu'on place la commande !
                    sh "ansible-playbook -i inventory.ini deploy.yml -e 'docker_image=riza239/app-flask-tp4:${BUILD_NUMBER}'"
                }
            }
        }

        stage('Smoke Test') {
            steps {
                echo "Waiting for app to be ready..."
                sh 'sleep 20'
                // On vérifie si le service répond
                sh 'kubectl get svc -n flask-prod'
                sh 'curl -f http://host.docker.internal:30001 || echo "App not reachable yet"'
            }
        }
    }
    
    // Optionnel : Nettoyage des images locales pour ne pas saturer le disque
    post {
        always {
            sh "docker rmi ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest || true"
        }
    }
}