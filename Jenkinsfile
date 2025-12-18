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
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        dvc pull
                    '''
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker build --no-provenance --no-sbom \
                          -t ${IMAGE_NAME}:latest .

                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy to GKE') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials anime-app-cluster --region us-central1
                        kubectl apply -f deployment.yaml
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up Docker...'
            sh '''
                docker image prune -a -f
                docker builder prune -f
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