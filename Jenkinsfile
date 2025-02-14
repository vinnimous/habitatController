@Library("security_stages") _

pipeline {
    agent any
    stages {
        stage('Setup') { // Install any dependencies you need to perform testing
            steps {
                script {
                sh """
                python3 -m venv ./venv
                . ./venv/bin/activate
                pip install -r requirements.txt
                """
                }
            }
        }
        stage('Test') { // Run the test scripts
            steps {
                script {
                sh """
                . ./venv/bin/activate
                pytest --cov=habitatController --cov-report=xml
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
    post {
        always {
            junit 'test-reports/*.xml'
            publishCoverage adapters: [coberturaAdapter('coverage.xml')]
        }
    }
}
