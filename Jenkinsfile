pipeline {
    agent {
        // Utilise un conteneur Python pour exécuter les étapes
        docker { 
            image 'python:3.9-slim' 
        }
    }

    environment {
        // 'SonarScanner' est le nom défini dans Manage Jenkins > Tools
        SONAR_SCANNER_HOME = tool 'SonarScanner' 
    }

    stages {
        stage('Checkout') {
            steps {
                // Récupère le code selon la config du Job Jenkins
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                // On installe les dépendances dans l'agent Docker
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
                // 'SonarQube' est le nom défini dans Manage Jenkins > System
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
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}