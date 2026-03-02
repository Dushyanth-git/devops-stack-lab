pipeline {
    agent any
    triggers {
        githubPush()
    }
    environment {
        DOCKERHUB_USERNAME = "dushyanth00"
        BACKEND_IMAGE = "${DOCKERHUB_USERNAME}/backend" 
        FRONTEND_IMAGE = "${DOCKERHUB_USERNAME}/frontend" 
        DEPLOY_HOST = "3.24.123.69"
        DEPLOY_PATH = "/home/ubuntu/app"
    }
    stages {
        stage('checkout'){
            steps{
                checkout scm  
                script{
                    env.SHORT_COMMIT = sh(
                        script: "git rev-parse --short HEAD",
                        returnStdout: true
                    ).trim()
                }
            }
        }
        stage('build backend image'){
            steps{
                sh """
                        docker build -t $BACKEND_IMAGE:$SHORT_COMMIT ./backend
                    """
            }
        }
        stage('build frontend image'){
            steps{
                sh """
                        docker build -t $FRONTEND_IMAGE:$SHORT_COMMIT ./frontend 
                    """

            }
        }
        stage('pushing images to dockerhub'){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
        )]) {
            sh 'echo "CREDENTIAL TEST SUCCESS"'
        }
    }
}
        stage('deploy-ec2-server'){
            steps{
                sshagent(['deploy-server-key']){
                    sh """
                        ssh -o StrictHostKeyChecking=no ubuntu@$DEPLOY_HOST '
                        echo IMAGE_TAG=$SHORT_COMMIT > $DEPLOY_PATH/.env &&
                        cd $DEPLOY_PATH &&
                        docker compose pull &&
                        docker compose up -d 
                    '
                    """
                }

            }
        }
    }
    post{
        always{
            sh "docker image prune -f"
        }
    }
}