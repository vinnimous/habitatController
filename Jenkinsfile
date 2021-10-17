pipeline {
    agent any
    stages {
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv(installationName: 'SonarQube', credentialsId: 'sonarqube-jenkins') {
                    sh '''$SCANNER_HOME/bin/sonar-scanner'''
                }
            }
        }
        stage("SonarQube quality gate") {
            steps {
                waitForQualityGate abortPipeline: true
            }
        }
    }
}