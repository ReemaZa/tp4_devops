pipeline {
    agent any

    environment {
        // Nom de la configuration configurée dans Manage Jenkins > System
        SONAR_SCANNER_HOME = tool 'SonarScanner' 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/votre-repo/app-flask.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python -m pytest test_app.py'
            }
        }

        stage('Static Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') { // 'SonarQube' est le nom du serveur configuré dans Jenkins
                    sh "${SONAR_SCANNER_HOME}/bin/sonar-scanner \
                    -Dsonar.projectKey=Flask_App_TP4 \
                    -Dsonar.sources=. \
                    -Dsonar.language=py"
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    // Attend que SonarQube finisse l'analyse et renvoie le statut
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}