pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = tool 'SonarScanner'
        DOCKER_HUB_USER = "riza239" // <-- À CHANGER
        IMAGE_NAME = "app-flask-tp4"
        REGISTRY_CREDS = "dockerhub-creds" // L'ID des credentials créés dans Jenkins
    }

    stages {
        stage('Install Dependencies') {
            steps {
                // On utilise python3 et pip3 installés à l'étape 1
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
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker tag ${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER} ${DOCKER_HUB_USER}/${IMAGE_NAME}:latest"
            }
        }

        stage('Image Scanning (Trivy)') {
            steps {
                // Scan de l'image. On ne bloque le pipeline que si c'est critique
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
    }
}