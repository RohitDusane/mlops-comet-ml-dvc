pipeline {
    agent any

    environment {
        GCP_PROJECT = 'credit-risk-071125'
        IMAGE_NAME = "gcr.io/${GCP_PROJECT}/anime-project"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
        DOCKER_BUILDKIT = '1'
        VENV_DIR = 'venv'
    }

    stages {

        stage('Clone Repository') {
            steps {
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'git-token',
                        url: 'https://github.com/RohitDusane/mlops-comet-ml-dvc.git'
                    ]]
                )
            }
        }


        stage('DVC Pull') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        python -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install dvc

                        export PATH=$PATH:/var/jenkins_home/google-cloud-sdk/bin
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project credit-risk-071125

                        dvc pull --run-cache
                    '''
                }
            }
        }


        stage('Build & Push Docker Image') {
            steps {
                script {
                    // Use BUILD_NUMBER as version tag
                    def versionTag = "${BUILD_NUMBER}"
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh """
                            export PATH=\$PATH:${GCLOUD_PATH}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            # Build Docker with BuildKit, multi-stage Dockerfile
                            docker build --build-arg GCP_PROJECT=${GCP_PROJECT} \
                                         --no-cache \
                                         --progress=plain \
                                         -t ${IMAGE_NAME}:${versionTag} .

                            # Tag latest
                            docker tag ${IMAGE_NAME}:${versionTag} ${IMAGE_NAME}:latest

                            # Push both tags
                            docker push ${IMAGE_NAME}:${versionTag}
                            docker push ${IMAGE_NAME}:latest
                        """
                    }
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                script {
                    def versionTag = "${BUILD_NUMBER}"
                    withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                        sh """
                            export PATH=\$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud container clusters get-credentials anime-app-cluster --region us-central1

                            # Apply config first
                            kubectl apply -f deployment.yaml

                            # Rolling update with new image tag
                            kubectl set image deployment/anime-app anime-app=${IMAGE_NAME}:${versionTag} --record
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker caches...'
            sh '''
                docker image prune -f --filter "until=24h"
                docker builder prune -f --filter "until=24h"
            '''
        }
    }
}




// pipeline {
//     agent any

//     environment{
//             VENV_DIR = 'venv'
//             GCP_PROJECT = 'credit-risk-071125'
//             GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
//             KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
//         }


//     stages{

//             stage("Cloning from Github...."){
//                 steps{
//                     script{
//                         echo 'Cloning from Github...'
//                         checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git-token', url: 'https://github.com/RohitDusane/mlops-comet-ml-dvc.git']])
//                     }
//                 }
//             }

//             stage("Making a virtual environment...."){
//                 steps{
//                     script{
//                         echo 'Making a virtual environment...'
//                         sh '''
//                         python -m venv ${VENV_DIR}
//                         . ${VENV_DIR}/bin/activate
//                         pip install --upgrade pip
//                         pip install -e .
//                         pip install  dvc
//                         '''
//                     }
//                 }
//             }


//             stage('DVC Pull'){
//                 steps{
//                     withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
//                         script{
//                             echo 'DVC Pul....'
//                             sh '''
//                             . ${VENV_DIR}/bin/activate
//                             dvc pull
//                             '''
//                         }
//                     }
//                 }
//             }


//             stage('Build and Push Image to GCR'){
//                 steps{
//                     withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
//                         script{
//                             echo 'Build and Push Image to GCR'
//                             sh '''
//                             export PATH=$PATH:${GCLOUD_PATH}
//                             gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
//                             gcloud config set project ${GCP_PROJECT}
//                             gcloud auth configure-docker --quiet
//                             docker build --no-provenance --no-sbom -t gcr.io/${GCP_PROJECT}/anime-project .
//                             docker push gcr.io/${GCP_PROJECT}/anime-project:latest
//                             '''
//                         }
//                     }
//                 }
//             }


//             stage('Deploying to Kubernetes'){
//                 steps{
//                     withCredentials([file(credentialsId:'gcp-key' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
//                         script{
//                             echo 'Deploying to Kubernetes'
//                             sh '''
//                             export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
//                             gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
//                             gcloud config set project ${GCP_PROJECT}
//                             gcloud container clusters get-credentials anime-app-cluster --region us-central1
//                             kubectl apply -f deployment.yaml
//                             '''
//                         }
//                     }
//                 }
//             }
//     }
// }