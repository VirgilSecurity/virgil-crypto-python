stage('Get Artifacts crypto lib python'){
    node('master'){
        print("Steps on master")
        clearContentUnix()

        checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'https://github.com/VirgilSecurity/virgil-crypto-python.git']]])

        step ([$class: 'CopyArtifact', projectName: 'VirgilCryptoLib-Staging', filter: '**']);


        stash includes: '**', excludes: 'install', name: 'wrapper-source'
        stash includes: 'install/python/virgil-crypto-**-linux**/**', excludes: '**.sha256', name: 'python-artifacts-linux'
        stash includes: 'install/python/virgil-crypto-**-windows**/**', excludes: '**.sha256', name: 'python-artifacts-windows'
        stash includes: 'install/python/virgil-crypto-**-darwin**/**', excludes: '**.sha256', name: 'python-artifacts-darwin'
    }
}

stage('Build'){
    def slaves = [:]
    slaves['native-linux'] = createLinuxWheels("build-docker", "linux")
    slaves['native-darwin'] = createLinuxWheels("build-docker", "osx")
    slaves['native-windows'] = createLinuxWheels("build-docker", "windows")
    parallel slaves
}

stage('Artifacts Packing'){
    node('master'){
        clearContentUnix()
        unstash 'linux-artifacts'
        unstash 'osx-artifacts'
        unstash 'windows-artifacts'
        archiveArtifacts("dist/**")
    }
}

// Utility Functions

def createLinuxWheels(slave, artifactType){
    return{
        if (artifactType == "linux"){
            node(slave){
                clearContentUnix()
                unstash 'wrapper-source'
                unstash 'python-artifacts-linux'
                def copiedFiles = []

                //x64
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7')
                docker.image("python:2.7").inside{
                    sh "python setup.py bdist_wheel"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.3")
                docker.image("python:3.3").inside{
                    sh "python setup.py bdist_wheel"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.4")
                docker.image("python:3.4").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                //x86
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7')
                docker.image("python:2.7").inside{
                    sh "python setup.py bdist_wheel --plat-name linux_i686"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.3")
                docker.image("python:3.3").inside{
                    sh "python setup.py bdist_wheel --plat-name linux_i686"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.4")
                docker.image("python:3.4").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name linux_i686"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                dir("dist"){
                    sh 'for file in *-cp27mu-*.whl; do cp $file ${file//cp27mu/cp27m}; done'
                }
                stash includes: "dist/**", name: "linux-artifacts"
            }
        }

        if (artifactType == "osx"){
            node(slave){
                clearContentUnix()
                unstash 'wrapper-source'
                unstash 'python-artifacts-darwin'
                def copiedFiles = []

                copiedFiles = unpackCryptoArtifactsLinux('python-2.7')
                docker.image("python:2.7").inside{
                    sh "python setup.py bdist_wheel --plat-name macosx_10_12_intel"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.4")
                docker.image("python:3.4").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name macosx_10_12_intel"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.5")
                docker.image("python:3.5").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name macosx_10_12_intel"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                //Fixing Python ABI tag
                dir("dist"){
                    sh 'for file in *-cp27mu-*.whl; do mv $file ${file//cp27mu/cp27m}; done'
                }

                stash includes: "dist/**", name: "osx-artifacts"
            }
        }

        if (artifactType == "windows"){
            node(slave){
                clearContentUnix()
                unstash 'wrapper-source'
                unstash 'python-artifacts-windows'
                def copiedFiles = []

                //x64
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7', "x64")
                docker.image("python:2.7").inside{
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.3", "x64")
                docker.image("python:3.3").inside{
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.4", "x64")
                docker.image("python:3.4").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.5", "x64")
                docker.image("python:3.5").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                //x86
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7', "x86")
                docker.image("python:2.7").inside{
                    sh "python setup.py bdist_wheel --plat-name win32"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.3", "x86")
                docker.image("python:3.3").inside{
                    sh "python setup.py bdist_wheel --plat-name win32"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.4", "x86")
                docker.image("python:3.4").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win32"
                }
                cleanBuildDirectoriesLinux(copiedFiles)

                copiedFiles = unpackCryptoArtifactsLinux("python-3.5", "x86")
                docker.image("python:3.5").inside{
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win32"
                }
                cleanBuildDirectoriesLinux(copiedFiles)


                //Fixing Python ABI tag
                dir("dist"){
                    sh 'for file in *-cp27mu-*.whl; do mv $file ${file//cp27mu/cp27m}; done'
                }

                stash includes: "dist/**", name: "windows-artifacts"
            }
        }
    }
}


def unpackCryptoArtifactsLinux(pythonVersionToUnpack){
    def copiedFiles = []
    sh "mkdir $WORKSPACE/temp_vars"
    dir("archive/install/python"){
        sh "ls -1 | grep $pythonVersionToUnpack | grep -E '^.*tgz\$' > $WORKSPACE/temp_vars/artifact_to_unpack.txt"
        def artifactToUnpack = readFile("$WORKSPACE/temp_vars/artifact_to_unpack.txt").trim()
        def artifactName = ""
        if (artifactToUnpack.endsWith(".tgz")){
            artifactName = artifactToUnpack.replace('.tgz', '')
            sh "tar xfz $artifactToUnpack"
        } else {
            artifactName = artifactToUnpack.replace('.zip', '')
            sh "unzip $artifactToUnpack"
        }

        if (artifactName){
            dir("$artifactName/lib/"){
                sh "ls -1 > $WORKSPACE/temp_vars/copied_file.txt"
            }
            copiedFiles << readFile("$WORKSPACE/temp_vars/copied_file.txt").trim()
            dir("$artifactName/api/"){
                sh "ls -1 > $WORKSPACE/temp_vars/copied_file.txt"
            }
            copiedFiles << readFile("$WORKSPACE/temp_vars/copied_file.txt").trim()
            sh "cp $artifactName/lib/* $WORKSPACE/virgil_crypto/"
            sh "cp $artifactName/api/* $WORKSPACE/virgil_crypto/"
            dir("$WORKSPACE/temp_vars"){
                deleteDir()
            }
        } else {
            print("WARNING: artifactName is EMPTY!")
        }
    }
    return copiedFiles
}

def unpackCryptoArtifactsLinux(pythonVersionToUnpack, platformArch){
    def copiedFiles = []
    sh "mkdir $WORKSPACE/temp_vars"
    dir("archive/install/python"){
        sh "ls -1 | grep $pythonVersionToUnpack | grep -E '^.*$platformArch.*zip\$' > $WORKSPACE/temp_vars/artifact_to_unpack.txt"
        def artifactToUnpack = readFile("$WORKSPACE/temp_vars/artifact_to_unpack.txt").trim()
        def artifactName = ""
        if (artifactToUnpack.endsWith(".tgz")){
            artifactName = artifactToUnpack.replace('.tgz', '')
            sh "tar xfz $artifactToUnpack"
        } else {
            artifactName = artifactToUnpack.replace('.zip', '')
            sh "unzip $artifactToUnpack"
        }

        if (artifactName){
            dir("$artifactName/lib/"){
                sh "ls -1 > $WORKSPACE/temp_vars/copied_file.txt"
            }
            copiedFiles << readFile("$WORKSPACE/temp_vars/copied_file.txt").trim()
            dir("$artifactName/api/"){
                sh "ls -1 > $WORKSPACE/temp_vars/copied_file.txt"
            }
            copiedFiles << readFile("$WORKSPACE/temp_vars/copied_file.txt").trim()
            sh "cp $artifactName/lib/* $WORKSPACE/virgil_crypto/"
            sh "cp $artifactName/api/* $WORKSPACE/virgil_crypto/"
            dir("$WORKSPACE/temp_vars"){
                deleteDir()
            }
        } else {
            print("WARNING: artifactName is EMPTY!")
        }
    }
    return copiedFiles
}

def cleanBuildDirectoriesLinux(copiedFiles){
    if (copiedFiles){
        for (copFile in copiedFiles){
            sh "rm virgil_crypto/$copFile"
        }
        dir("build"){
            deleteDir()
        }
        dir("*.egg-info"){
            deleteDir()
        }
    } else {
        print("WARNING! Nothing to do copiedFiles EMPTY!")
    }
}

def clearContentUnix() {
    sh "rm -fr -- *"
}


def archiveArtifacts(pattern) {
    step([$class: 'ArtifactArchiver', artifacts: pattern, fingerprint: true, onlyIfSuccessful: true])
}
