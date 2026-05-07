pipeline {
    agent any

    environment {
        SONAR_SCANNER_HOME = tool 'SonarScanner' 
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
}