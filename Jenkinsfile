pipeline{
    agent any 
    stages{
        stage('git checkout'){
            steps{
                git branch: 'main', url: 'https://github.com/Dushyanth-git/devops-practice-app.git'
            }
        }
        stage('build and compose up'){
            steps{
                sh 'docker compose down'
                sh 'docker compose up -d --build'
            }
        }
    }
}