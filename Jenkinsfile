pipeline {
    agent any
    stages {
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv(installationName: 'SonarQube', credentialsId: 'sonarqube-jenkins') {
                    sh '''${SONAR_SCANNER} -Dproject.settings=sonar-project.properties'''
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