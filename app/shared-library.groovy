// this type of thing should go in a shared library in the future
// https://jenkins.io/doc/book/pipeline/shared-libraries/

import groovy.json.JsonOutput;

def patchBuildConfigOutputLabels(env) {

    // needed because https://github.com/openshift/jenkins/issues/574
    // TODO maybe move to jenkins client? I dunno, that client feels flaky...
    def jenkinsHost = sh(script: "oc get route jenkins --template={{.spec.host}} -n ${env.CI_CD_NAMESPACE}", returnStdout: true)

    def patch = [
            spec: [
                output : [
                    imageLabels : [ 
                        [ name: 'io.openinnovationlabs.jenkins.build.url', value: "${env.RUN_DISPLAY_URL}".replace('unconfigured-jenkins-location', jenkinsHost) ],
                        [ name: 'io.openinnovationlabs.jenkins.build.tag', value: "${env.BUILD_NUMBER}"],
                        [ name: 'io.openinnovationlabs.git.branch', value: "${env.GIT_BRANCH}"],
                        [ name: 'io.openinnovationlabs.git.url', value: "${env.GIT_URL}"],
                        [ name: 'io.openinnovationlabs.git.commit', value: "${env.GIT_COMMIT}"]
                    ]
                ]
            ] 
        ]
    def patchJson = JsonOutput.toJson(patch)

    // TODO maybe move to jenkins client? I dunno, that client feels flaky...
    sh "oc patch bc ${APP_NAME} -p '${patchJson}' -n ${env.CI_CD_NAMESPACE}"
}

/*
    There seems to be some instability with this approach, even though it's exactly the same impl from the old plugin
    The logging is crappy in the client, so very hard to debug what the failure is at the moment.
*/
def verifyDeployment(String appName, String projectName ){     
    openshift.withCluster () {
        echo "Verifying deployment with project " + projectName + " of app " + appName + " 10 second wait"
        sleep 10 // give the deployment a few seconds. Will never complete that fast
        openshift.withProject( projectName ){
            def latestDeploymentVersion = openshift.selector('dc', appName ).object().status.latestVersion
            echo "Latest version " + latestDeploymentVersion
            def rc = openshift.selector('rc', "${appName}-${latestDeploymentVersion}")
            
            echo "rc"
            echo rc.toString()
            rc.untilEach(1){
                def rcMap = it.object()
                echo "Saw " + rcMap.status.replicas.equals(rcMap.status.readyReplicas)
                return (rcMap.status.replicas.equals(rcMap.status.readyReplicas))
            }
        }
    }
    echo "Verification complete"
}

def promoteImageWithinCluster( String appName, String sourceProjectName, String targetProjectName ){
    openshift.withCluster () {
        try {
            echo "Tagging ${targetProjectName}/${appName}:latest ${targetProjectName}/${appName}:previous"
            openshift.tag( "${targetProjectName}/${appName}:latest ${targetProjectName}/${appName}:previous" )
        } catch (Exception ex) {
            echo 'Failed to tag for previous'
        }
        echo "Tagging ${sourceProjectName}/${appName}:latest ${targetProjectName}/${appName}:latest"
        openshift.tag( "${sourceProjectName}/${appName}:latest ${targetProjectName}/${appName}:latest" )
        echo "Tagging ${sourceProjectName}/${appName}:latest ${targetProjectName}/${appName}:deployed"
        openshift.tag( "${sourceProjectName}/${appName}:latest ${targetProjectName}/${appName}:deployed" )
    }
}


def applyAnsibleInventory( String tag ){
    sh """
        cd .openshift-applier
        ansible-galaxy install -r requirements.yml --roles-path=roles
        ansible-playbook -i inventory/ apply.yml -e filter_tags=${tag}
    """
}
return this;