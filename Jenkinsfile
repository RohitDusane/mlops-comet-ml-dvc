pipeline {
    agent any

    options {
        disableResume()                     // Prevent resumed-build durable-task failures
        timestamps()
        timeout(time: 60, unit: 'MINUTES')  // Global safety timeout
    }

    environment {
        VENV_DIR = 'venv'
    }

    stages {

        stage("Cloning from Github") {
            steps {
                echo 'Cloning from Github...'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'git-token',
                        url: 'https://github.com/RohitDusane/mlops-comet-ml-dvc.git'
                    ]]
                )
            }
        }

        stage("Installing Dependencies") {
            options {
                timeout(time: 30, unit: 'MINUTES')   // Avoid silent long-running hangs
            }
            steps {
                script {
                    catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {

                        echo 'Setting up Python virtual environment...'

                        sh '''
                        set -euo pipefail

                        # Create the virtual environment
                        python -m venv ${VENV_DIR}

                        # Activate
                        . ${VENV_DIR}/bin/activate

                        # Ensure pip is chatty so Jenkins sees output
                        pip install --upgrade pip --progress-bar=on

                        # Install UI dependencies first (non-heavy)
                        pip install colorama==0.4.5 --progress-bar=on

                        # Install lightweight requirements
                        pip install -r requirements.txt --no-cache-dir --progress-bar=on

                        # Install TensorFlow separately so we can monitor it
                        echo "Installing TensorFlow (this may take several minutes)..."
                        pip install tensorflow-cpu==2.20.0 --no-cache-dir --progress-bar=on -v

                        # Install DVC
                        pip install dvc --progress-bar=on
                        '''
                    }
                }
            }
        }

        stage('DVC Pull') {
            steps {
                withCredentials([
                    file(credentialsId: 'anime-gcp', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {
                    script {
                        echo 'Running DVC Pull...'
                        sh '''
                        set -euo pipefail
                        . ${VENV_DIR}/bin/activate
                        dvc pull -v
                        '''
                    }
                }
            }
        }
    }
}




// pipeline {
//     agent any

//     environment{
//             VENV_DIR = 'venv'
//             // GCP_PROJECT = 'credit-risk-071125'
//             // GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
//             // KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
//         }

//     stages{

//         stage("Cloning from Github...."){
//             steps{
//                 script{
//                     echo 'Cloning from Github...'
//                     checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'git-token', url: 'https://github.com/RohitDusane/mlops-comet-ml-dvc.git']])
                    
//                 }
//             }
//         }

//         // stage("Making a virtual environment....") {
//         //     steps {
//         //         script {
//         //             catchError(buildResult: 'FAILURE', stageResult: 'FAILURE')
//         //             echo 'Making a virtual environment...'
//         //             sh '''
//         //             # Create the virtual environment
//         //             python -m venv ${VENV_DIR}

//         //             # Activate the virtual environment and install dependencies
//         //             . ${VENV_DIR}/bin/activate

//         //             # Upgrade pip and install the required packages
//         //             pip install --upgrade pip
//         //             pip install -r requirements.txt
//         //             pip install dvc
//         //             '''
//         //         }
//         //     }
//         // }
        

//         stage("Making a virtual environment....") {
//             steps {
//                 script {
//                     catchError(buildResult: 'FAILURE', stageResult: 'FAILURE') {
//                         echo 'Making a virtual environment...'
//                         sh '''
//                         # Create the virtual environment
//                         python -m venv ${VENV_DIR}

//                         # Activate the virtual environment and install dependencies
//                         . ${VENV_DIR}/bin/activate

//                         # Upgrade pip and install the required packages
//                         pip install --upgrade pip
//                         pip install -r requirements.txt --no-cache-dir
//                         pip install --progress-bar=on --no-cache-dir tensorflow-cpu==2.20.0
//                         pip install colorama==0.4.5
//                         pip install dvc
//                         '''

//                     }
//                 }
//             }
//         }


//         stage('DVC Pull'){
//             steps{
//                 withCredentials([file(credentialsId: 'anime-gcp' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
//                     script{
//                         echo 'DVC Pull....'
//                         sh '''
//                         . ${VENV_DIR}/bin/activate
//                         dvc pull
//                         '''
//                     }
//                 }
//             }
//         }



//         // stage('Build and Push Image to GCR'){
//         //     steps{
//         //         withCredentials([file(credentialsId: 'anime-gcp', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
//         //             script{
//         //                 echo 'Build and Push Image to GCR'
//         //                 sh '''
//         //                 export PATH=$PATH:${GCLOUD_PATH}
//         //                 gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
//         //                 gcloud config set project ${GCP_PROJECT}
//         //                 gcloud auth configure-docker --quiet
                        
//         //                 # Build and push docker image to GCR
//         //                 docker build --no-cache -t gcr.io/credit-risk-071125/anime-project:latest -f Dockerfile .
//         //                 docker push gcr.io/${GCP_PROJECT}/anime-project:latest
//         //                 '''
//         //             }
//         //         }
//         //     }
//         // }


//         // stage('Deploying to Kubernetes'){
//         //     steps{
//         //         withCredentials([file(credentialsId: 'anime-gcp' , variable: 'GOOGLE_APPLICATION_CREDENTIALS' )]){
//         //             script{
//         //                 echo 'Deploying to Kubernetes'
//         //                 sh '''
//         //                 export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
//         //                 gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
//         //                 gcloud config set project ${GCP_PROJECT}
//         //                 gcloud container clusters get-credentials anime-app-cluster --region us-central1
//         //                 kubectl apply -f deployment.yaml
//         //                 '''
//         //             }
//         //         }
//         //     }        
//         // }
        
//     }
// }