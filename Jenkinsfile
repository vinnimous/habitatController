pipeline {
    agent any
    stages {
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv(installationName: 'SonarQube', credentialsId: 'sonarqube') {
                    sh '''${SONAR_SCANNER}
                        -Dproject.settings=sonar-project.properties
                        // -Dsonar.branch.name=${BRANCH_NAME}
                        '''
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
