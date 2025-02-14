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
                pip install -r requirements.txt pytest pytest-cov
                mkdir -p test-reports
                """
                }
            }
        }
        stage('Test') { // Run the test scripts
            steps {
                script {
                sh """
                . ./venv/bin/activate
                which pytest
                pytest --cov=habitatController --junitxml=test-reports/results.xml --cov-report=xml
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
            // Debug steps to check the existence and contents of the test report file
            script {
                sh """
                echo "Checking if test report exists:"
                ls -l test-reports/results.xml
                echo "Displaying contents of the test report:"
                cat test-reports/results.xml
                """
            }
            junit 'test-reports/results.xml'
            publishCoverage adapters: [coberturaAdapter('coverage.xml')]
        }
    }
}
