@Library("security_stages") _

pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: "3", artifactNumToKeepStr: "3"))
    }

    stages {
        stage('Setup') { // Install any dependencies you need to perform testing
            steps {
                script {
                sh """
                python3 -m venv ./venv
                . ./venv/bin/activate
                pip install -r requirements.txt pytest pytest-cov
                mkdir -p test-reports
                """
                }
            }
        }
        stage ("Attempting security stages") {
            steps {
                shared()
            }
        }
    }
}
