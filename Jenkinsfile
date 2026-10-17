pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
    }

    environment {
        COMPOSE_PROJECT_NAME = 'qa-jenkins'
        POSTGRES_USER = 'qa_user'
        POSTGRES_PASSWORD = 'jenkins_only_password'
        POSTGRES_DB = 'qa_db'
        POSTGRES_PORT = '5433'
    }

    stages {
        stage('Lint') {
            steps {
                sh 'docker compose -f compose.yaml build tests'
                sh 'docker compose -f compose.yaml run --rm --no-deps tests sh -c "ruff check . && ruff format --check ."'
            }
        }

        stage('Tests') {
            steps {
                sh '''
                    rm -rf allure-results junit.xml
                    docker rm -f qa-tests || true
                    docker compose -f compose.yaml up -d --build --wait app
                    set +e
                    docker compose -f compose.yaml run --name qa-tests tests pytest -n 2 --junitxml=/app/junit.xml
                    status=$?
                    set -e
                    docker cp qa-tests:/app/junit.xml junit.xml || true
                    docker cp qa-tests:/app/allure-results allure-results || true
                    docker rm -f qa-tests || true
                    exit $status
                '''
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'junit.xml'
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            sh 'docker compose -f compose.yaml logs --no-color > compose.log || true'
            archiveArtifacts artifacts: 'compose.log', allowEmptyArchive: true
            sh 'docker compose -f compose.yaml --profile tests down -v || true'
        }
    }
}