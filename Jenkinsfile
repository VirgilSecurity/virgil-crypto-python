// --------------------------------------------------------------------------
//  Configuration properties.
// --------------------------------------------------------------------------
properties([
    parameters([
        booleanParam(name: 'DEPLOY_ARTIFACTS', defaultValue: false,
            description: 'If branch = master and build succeeded then Python artifacts will be deployed to the Pip repository..')
    ])
])

stage('Grab SCM'){
    node('master'){
        clearContentUnix()
        checkout scm
        stash includes: "**", name: "python_source"
    }
}

stage('Build'){
    node("build-docker"){
        // Build python wheels
        docker.image("python:3.7").inside("--user root"){
            cleanPythonPackageBuildDirectoriesLinux()
            sh "pip install wheel"
            sh "python setup.py bdist_wheel --universal"
        }

        // Build python eggs
        docker.image("python:2.7").inside("--user root"){
            cleanPythonPackageBuildDirectoriesLinux()
            sh "python setup.py bdist_egg"
        }

        docker.image("python:3.4").inside("--user root"){
            cleanPythonPackageBuildDirectoriesLinux()
            sh "python setup.py bdist_egg"
        }

        docker.image("python:3.5").inside("--user root"){
            cleanPythonPackageBuildDirectoriesLinux()
            sh "python setup.py bdist_egg"
        }

        docker.image("python:3.6").inside("--user root"){
            cleanPythonPackageBuildDirectoriesLinux()
            sh "python setup.py bdist_egg"
        }

        docker.image("python:3.7").inside("--user root"){
            cleanPythonPackageBuildDirectoriesLinux()
            sh "python setup.py bdist_egg"
        }
    stash includes: "dist/**", name: "python-packages"
    }
}

stage('Artifacts Packing'){
    node('master'){
        clearContentUnix()
        unstash 'python-packages'
        archiveArtifacts("dist/**")
    }
}

stage('Deploy Packages'){
    node('master') {
        clearContentUnix()
        unstash 'python-packages'

        echo "DEPLOY_ARTIFACTS = ${params.DEPLOY_ARTIFACTS}"
        if (!params.DEPLOY_ARTIFACTS) {
            echo "Skipped due to the false parameter: DEPLOY_ARTIFACTS"
            return
        }

        if (env.BRANCH_NAME == "master") {
            sh """
                env
                twine upload dist/*
            """
        } else {
            echo "Skipped due to the branch: $BRANCH_NAME is not master"
            return
        }
    }
}

// Utility Functions

def cleanPythonPackageBuildDirectoriesLinux(){
    sh "find virgil_crypto_lib/ -name '*.pyc' -delete"
    sh "rm -rf ./build"
    sh "rm -rf *.egg-info"
}

def clearContentUnix() {
    sh "rm -fr -- *"
}


def archiveArtifacts(pattern) {
    step([$class: 'ArtifactArchiver', artifacts: pattern, fingerprint: true, onlyIfSuccessful: true])
}
