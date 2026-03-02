pipeline {
    agent any
    triggers {
        githubPush()
    }
    environment {
        DOCKERHUB_USERNAME = "dushyanth00"
        BACKEND_IMAGE = "${DOCKERHUB_USERNAME}/backend" 
        FRONTEND_IMAGE = "${DOCKERHUB_USERNAME}/frontend" 
        DEPLOY_HOST = ""
        DEPLOY_PATH = "/home/ubuntu/app"
    }
    stages {
        stage('checkout'){
            steps{
                checkout scm 
            }
        }
        stage('build backend image'){
            SHORT_COMMIT = "${env.GIT_COMMIT[0..6]}"
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
        stage('pushing images to dockerhub '){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]){
                    sh """
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push $BACKEND_IMAGE:$SHORT_COMMIT
                        docker push $FRONTEND_IMAGE:$SHORT_COMMIT
                        docker logout
                    """
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