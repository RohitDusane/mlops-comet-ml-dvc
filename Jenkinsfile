pipeline {
    agent any

    // environment {
    //     VENV_DIR = 'venv'
    //     GCP_PROJECT = 'mlops-new-447207'
    //     GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    //     KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
    // }

    stages{

        stage("Cloning from Github...."){
            steps{
                script{
                    echo 'Cloning from Github...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-tokens-2', url: 'https://github.com/RohitDusane/mlops-comet-ml-dvc.git']])
                }
            }
        }

        stage("Making a virtual environment...."){
            steps{
                script{
                    echo 'Making a virtual environment...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install  dvc
                    '''
                }
            }
        }







        
    }
}