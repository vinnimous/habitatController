pipeline {
    agent any
    stages {
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv('SonarQube')
                sonar-scanner
            }
        }
        stage("SonarQube quality gate") {
            steps {
                waitForQualityGate abortPipeline: true
            }
        }
    }
}