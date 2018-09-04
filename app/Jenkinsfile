pipeline {

    agent {
        label "master"
    }

    environment {
        // Global Vars
        PIPELINES_NAMESPACE = "labs-ci-cd"
        APP_NAME = "flask"

        JENKINS_TAG = "${JOB_NAME}.${BUILD_NUMBER}".replace("/", "-")
        JOB_NAME = "${JOB_NAME}".replace("/", "-")
        NEXUS_SERVICE_HOST = 'nexus'
        NEXUS_SERVICE_PORT = '8081'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr:'10'))
        timeout(time: 15, unit: 'MINUTES')
        ansiColor('xterm')
        timestamps()
    }

    stages {
        stage("prepare environment for master deploy") {
            agent {
                node {
                    label "master"
                }
            }
            when {
              expression { GIT_BRANCH ==~ /(.*master)/ }
            }
            steps {
                script {
                    env.PROJECT_NAMESPACE = "flask-test"
                    env.FLASK_ENV = "test"
                }
            }
        }
        stage("prepare environment for develop deploy") {
            agent {
                node {
                    label "master"
                }
            }
            when {
              expression { GIT_BRANCH ==~ /(.*develop)/ }
            }
            steps {
                script {
                    env.PROJECT_NAMESPACE = "flask-dev"
                    env.FLASK_ENV = "dev"
                }
            }
        }
        stage("test and build") {
            agent {
                node {
                    label "jenkins-slave-python"  
                }
            }
            steps {
                sh 'python --version'
                //sh 'python -m virtualenv env'
                //sh 'source env/bin/activate'
                sh 'pip install -r requirements.txt --user'
                sh 'pytest --junitxml=test-report.xml'
                sh 'zip -r package-contents.zip .'
                sh 'curl -vvv -u admin:admin123 --upload-file package-contents.zip http://${NEXUS_SERVICE_HOST}:${NEXUS_SERVICE_PORT}/repository/zip/com/redhat/${APP_NAME}/${JOB_NAME}.${BUILD_NUMBER}/package-contents.zip'
            }
            post {
                always {
                    archive "**"
                    junit 'test-report.xml'
                    // publish html

                    // Notify slack or some such
                }
                success {
                    echo "Woo!"
                }
                failure {
                    echo "FAILURE"
                }
            }
        }
        stage("bake image") {
            agent {
                node {
                    label "master"  
                }
            }
            when {
                expression { GIT_BRANCH ==~ /(.*master|.*develop)/ }
            }
            steps {
                echo '### Get Binary from Nexus ###'
                sh  '''
                        rm -rf package-contents*
                        curl -v -f http://admin:admin123@${NEXUS_SERVICE_HOST}:${NEXUS_SERVICE_PORT}/repository/zip/com/redhat/${APP_NAME}/${JENKINS_TAG}/package-contents.zip -o package-contents.zip
                        unzip package-contents.zip
                    '''
                echo '### Create Linux Container Image from package ###'
                sh  '''
                        oc project ${PIPELINES_NAMESPACE} # probs not needed
                        oc patch bc ${APP_NAME} -p "{\\"spec\\":{\\"output\\":{\\"to\\":{\\"kind\\":\\"ImageStreamTag\\",\\"name\\":\\"${APP_NAME}:${JENKINS_TAG}\\"}}}}"
                        oc start-build ${APP_NAME} --from-dir=package-contents/ --follow
                    '''
            }
            post {
                always {
                    archive "**"
                }
            }
        }
        stage("deploy") {
            agent {
                node {
                    label "master"  
                }
            }
            when {
                expression { GIT_BRANCH ==~ /(.*master|.*develop)/ }
            }
            steps {
                echo '### tag image for namespace ###'
                sh  '''
                    oc project ${PROJECT_NAMESPACE}
                    oc tag ${PIPELINES_NAMESPACE}/${APP_NAME}:${JENKINS_TAG} ${PROJECT_NAMESPACE}/${APP_NAME}:${JENKINS_TAG}
                    '''
                echo '### set env vars and image for deployment ###'
                sh '''
                    oc set image dc/${APP_NAME} ${APP_NAME}=docker-registry.default.svc:5000/${PROJECT_NAMESPACE}/${APP_NAME}:${JENKINS_TAG}
                    oc rollout latest dc/${APP_NAME}
                '''
                echo '### Verify OCP Deployment ###'
                openshiftVerifyDeployment depCfg: env.APP_NAME, 
                    namespace: env.PROJECT_NAMESPACE, 
                    replicaCount: '1', 
                    verbose: 'false', 
                    verifyReplicaCount: 'true', 
                    waitTime: '',
                    waitUnit: 'sec'
            }
        }
    }
}