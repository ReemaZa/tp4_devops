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
                    -Dsonar.language=py \
                    -Dsonar.exclusions=**/*.yaml,**/*.tf,test_app.py \
                    -Dsonar.python.coverage.reportPaths=coverage.xml"
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

        stage('Deploy App & Monitoring') {
            steps {
                // 1. Dépendances Python pour Ansible
                sh '/usr/bin/python3.13 -m pip install kubernetes --break-system-packages'
                sh 'ansible-galaxy collection install kubernetes.core'
                
                // 2. Déploiement des Pods (Deployment) via Ansible
                dir('ansible') {
                    sh "ansible-playbook -i inventory.ini deploy.yml -e 'docker_image=${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}'"
                }

                // 3. Application de TOUTE la configuration K8s (Service, Monitoring, Alertes)
                echo "Applying K8s manifests from folder..."
                // On applique tout le dossier k8s d'un coup
                sh 'kubectl apply -f k8s/'
            }
        }

        stage('Verify & Observability Check') {
            steps {
                echo "Waiting for pods to be ready..."
                sh 'kubectl wait --for=condition=ready pod -l app=flask -n flask-prod --timeout=60s'
                
                echo "Verifying Monitoring Resources:"
                // On vérifie que nos nouveaux objets sont bien créés
                sh 'kubectl get servicemonitor -n monitoring'
                sh 'kubectl get prometheusrules -n monitoring'
                
                echo "Check internal app endpoint:"
                sh 'curl -s http://host.docker.internal:30001/metrics || echo "Metrics endpoint not ready"'
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