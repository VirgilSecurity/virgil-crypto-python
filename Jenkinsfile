def CRYPTO_VERSION = "undefined"

stage('Get Artifacts crypto lib python'){
    node('master'){
        clearContentUnix()
        checkout scm

        step ([$class: 'CopyArtifact', projectName: "$CRYPTO_ARTIFACTS_NAME", filter: 'install/python/**']);
        step ([$class: 'CopyArtifact', projectName: "$CRYPTO_ARTIFACTS_NAME", filter: 'install/VERSION']);
        CRYPTO_VERSION = readFile("install/VERSION")
        sh "rm install/VERSION"
        stash excludes: '**/install/**', includes: '**', name: 'wrapper-source'
        stash excludes: '*.sha256', includes: 'install/python/virgil-crypto-**-linux**', name: 'python-artifacts-linux'
        stash excludes: '*.sha256', includes: 'install/python/virgil-crypto-**-windows**', name: 'python-artifacts-windows'
        stash excludes: '*.sha256', includes: 'install/python/virgil-crypto-**-darwin**', name: 'python-artifacts-darwin'
    }
}

stage('Build'){
    echo("Version of Crypto build: $CRYPTO_VERSION")
    def slaves = [:]
    slaves['native-linux'] = createLinuxWheels("build-docker", "linux", CRYPTO_VERSION)
    slaves['native-darwin'] = createLinuxWheels("build-docker", "osx", CRYPTO_VERSION)
    slaves['native-windows'] = createLinuxWheels("build-docker", "windows", CRYPTO_VERSION)
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

def createLinuxWheels(slave, artifactType, CRYPTO_VERSION){
    return{
        if (artifactType == "linux"){
            node(slave){
                docker.image('python:2.7').inside("--user root"){
                    clearContentUnix()
                }
                unstash 'wrapper-source'
                unstash 'python-artifacts-linux'
                def copiedFiles = []

                //x64
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7')
                docker.image("python:2.7").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name manylinux1_x86_64"
                    sh "python setup.py bdist_egg --plat-name manylinux1_x86_64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.3")
                docker.image("python:3.3").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name manylinux1_x86_64"
                    sh "python setup.py bdist_egg --plat-name manylinux1_x86_64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.4")
                docker.image("python:3.4").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name manylinux1_x86_64"
                    sh "python setup.py bdist_egg --plat-name manylinux1_x86_64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                copiedFiles = unpackCryptoArtifactsLinux("python-3.5")
                docker.image("python:3.5").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name manylinux1_x86_64"
                    sh "python setup.py bdist_egg --plat-name manylinux1_x86_64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                copiedFiles = unpackCryptoArtifactsLinux("python-3.6")
                docker.image("python:3.6").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name manylinux1_x86_64"
                    sh "python setup.py bdist_egg --plat-name manylinux1_x86_64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                //x86
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7')
                docker.image("python:2.7").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name manylinux1_i686"
                    sh "python setup.py bdist_egg --plat-name manylinux1_i686"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.3")
                docker.image("python:3.3").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name manylinux1_i686"
                    sh "python setup.py bdist_egg --plat-name manylinux1_i686"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.4")
                docker.image("python:3.4").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name manylinux1_i686"
                    sh "python setup.py bdist_egg --plat-name manylinux1_i686"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                copiedFiles = unpackCryptoArtifactsLinux("python-3.5")
                docker.image("python:3.5").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name manylinux1_i686"
                    sh "python setup.py bdist_egg --plat-name manylinux1_i686"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                copiedFiles = unpackCryptoArtifactsLinux("python-3.6")
                docker.image("python:3.6").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name manylinux1_i686"
                    sh "python setup.py bdist_egg --plat-name manylinux1_i686"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                stash includes: "dist/**", name: "linux-artifacts"
            }
        }

        if (artifactType == "osx"){
            node(slave){
                docker.image('python:2.7').inside("--user root"){
                    clearContentUnix()
                }
                unstash 'wrapper-source'
                unstash 'python-artifacts-darwin'
                def copiedFiles = []

                copiedFiles = unpackCryptoArtifactsLinux('python-2.7')
                docker.image("python:2.7").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name macosx_10_12_intel"
                    sh "python setup.py bdist_egg --plat-name macosx_10_12_intel"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.4")
                docker.image("python:3.4").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name macosx_10_12_intel"
                    sh "python setup.py bdist_egg --plat-name macosx_10_12_intel"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.5")
                docker.image("python:3.5").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name macosx_10_12_intel"
                    sh "python setup.py bdist_egg --plat-name macosx_10_12_intel"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                copiedFiles = unpackCryptoArtifactsLinux("python-3.6")
                docker.image("python:3.6").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name macosx_10_12_intel"
                    sh "python setup.py bdist_egg --plat-name macosx_10_12_intel"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                //Fixing Python ABI tag
                docker.image("python:2.7").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh 'for file in dist/*-cp27mu-*.whl; do mv $file ${file//cp27mu/cp27m}; done'
                }

                stash includes: "dist/**", name: "osx-artifacts"
            }
        }

        if (artifactType == "windows"){
            node(slave){
                docker.image('python:2.7').inside("--user root"){
                    clearContentUnix()
                }
                unstash 'wrapper-source'
                unstash 'python-artifacts-windows'
                def copiedFiles = []

                //x64
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7', "x64")
                docker.image("python:2.7").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                    sh "python setup.py bdist_egg --plat-name win_amd64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.3", "x64")
                docker.image("python:3.3").inside("--user root  --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                    sh "python setup.py bdist_egg --plat-name win_amd64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.4", "x64")
                docker.image("python:3.4").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                    sh "python setup.py bdist_egg --plat-name win_amd64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.5", "x64")
                docker.image("python:3.5").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                    sh "python setup.py bdist_egg --plat-name win_amd64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                copiedFiles = unpackCryptoArtifactsLinux("python-3.6", "x64")
                docker.image("python:3.6").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win_amd64"
                    sh "python setup.py bdist_egg --plat-name win_amd64"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                //x86
                copiedFiles = unpackCryptoArtifactsLinux('python-2.7', "x86")
                docker.image("python:2.7").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name win32"
                    sh "python setup.py bdist_egg --plat-name win32"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.3", "x86")
                docker.image("python:3.3").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "python setup.py bdist_wheel --plat-name win32"
                    sh "python setup.py bdist_egg --plat-name win32"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.4", "x86")
                docker.image("python:3.4").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win32"
                    sh "python setup.py bdist_egg --plat-name win32"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }


                copiedFiles = unpackCryptoArtifactsLinux("python-3.5", "x86")
                docker.image("python:3.5").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win32"
                    sh "python setup.py bdist_egg --plat-name win32"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                copiedFiles = unpackCryptoArtifactsLinux("python-3.6", "x86")
                docker.image("python:3.6").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh "pip install wheel"
                    sh "python setup.py bdist_wheel --plat-name win32"
                    sh "python setup.py bdist_egg --plat-name win32"
                    cleanBuildDirectoriesLinux(copiedFiles)
                }

                //Fixing Python ABI tag
                docker.image("python:2.7").inside("--user root --env CRYPTO_VERSION=$CRYPTO_VERSION"){
                    sh 'for file in dist/*-cp27mu-*.whl; do mv $file ${file//cp27mu/cp27m}; done'
                }

                stash includes: "dist/**", name: "windows-artifacts"
            }
        }
    }
}


def unpackCryptoArtifactsLinux(pythonVersionToUnpack){
    def copiedFiles = []
    sh "mkdir $WORKSPACE/temp_vars"
    dir("install/python"){
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
    dir("install/python"){
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
        sh "rm -r ./build"
        sh "rm -r *.egg-info"
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
