def call(body) {
    def pipelineParams= [:]
    body.resolveStrategy = Closure.DELEGATE_FIRST
    body.delegate = pipelineParams
    body()

    pipeline {
        agent { label 'docker' }
        options {
            timestamps()
            //logging (
            //    pollLogging :true
                //pruneDays : 20
                //target : {
                //    name 'org.techworld.sonar'
                //    level 'FINE'
                //s)
            //)
        }
        parameters {

            choice(name: 'branchName', choices: ['debug', 'release', 'feature'], description: 'Pick something')
        }
    
        stages {
            stage('Stage_1') {
                agent any
                options { timestamps() }
            
                steps {
                    myTask()
                }
                post {
                    always {
                        archiveArtifacts artifacts: "Build_${BUILD_ID}_*.log", fingerprint: true, followSymlinks: false
                    }
                }
            }

            stage('Stages 2 and 3') {
                parallel {
                    stage('Stage_2') {
                        /*agent {
                            dockerfile {
                                filename 'Dockerfile'
                                //dir 'jenkins/shared/github-api-global-lib/resources/com/planetpope/Dockerfiles'
                                dir "."
                                // label 'my-defined-label' // Queued There are no nodes with the label ‘my-defined-label’
                                additionalBuildArgs '--build-arg version=1.0.2'
                                args '-v /tmp:/tmp'
                            }

                            //docker { image 'ubuntu:24.04' }
                        }*/
                        agent { label 'docker' }

                        steps {
                            //myTask()
                            myDocker()
                        }
                        post {
                            always {
                                archiveArtifacts artifacts: "Build_${BUILD_ID}_*.log", fingerprint: true, followSymlinks: false
                            }
                        }
                    } // stage('Stage_2')


                    stage('Stage_3') {
                        agent any
                        when {
                            expression {
                                return branchName == 'release' || branchName == 'feature';
                            }
                        }
                        steps {
                            myTask()
                        }
                        post {
                            always {
                                archiveArtifacts artifacts: "Build_${BUILD_ID}_*.log", fingerprint: true, followSymlinks: false
                            }
                        }                    
                    } // stage('Stage_3')

                } // parallel
            } // stage('Stages 2 and 3')
        }
        /*post {
            always {
                archiveArtifacts artifacts: 'pipeline.log', fingerprint: true, followSymlinks: false
            }
        }*/
    }
}


def myDocker()
{
    //checkout scm

    def scriptcontents = libraryResource "com/planetpope/Dockerfiles/myDockerFile"    
    sh "pwd"
    sh "ls -la"
    writeFile file: "Dockerfile", text: scriptcontents
    sh "chmod a+x ./Dockerfile"
    sh "pwd"
    sh "ls -la"

    //def dockerFile = 'jenkins/shared/github-api-global-lib/resources/com/planetpope/Dockerfiles/myDockerFile'
    def dockerFile = './Dockerfile'
    def imageName = "my-image:${env.BUILD_ID}"
    def dockerArgs = " --pull --rm ${pwd}"
    def imageArgs = "-f ${dockerFile} ${dockerArgs}"
    def customImage = docker.build(imageName, imageArgs)

    customImage.inside {
        //sh 'make test'
        myTask()
    } 
}


def myTask()
{
    echo "${STAGE_NAME}"
    sh 'lsb_release -a'
    sh 'uname -a'
    sh 'printenv'
    
    sh "echo ${STAGE_NAME} > Build_${BUILD_ID}_${STAGE_NAME}.log"
    sh "echo ${BUILD_TIMESTAMP} >> Build_${BUILD_ID}_${STAGE_NAME}.log"
    //echo "'\n' > Build_${BUILD_ID}_${STAGE_NAME}.log"
    sh "echo \$(lsb_release -a) >> Build_${BUILD_ID}_${STAGE_NAME}.log"
    sh "echo \$(uname -a) >> Build_${BUILD_ID}_${STAGE_NAME}.log"
    //echo "'\n' > Build_${BUILD_ID}_${STAGE_NAME}.log"
    sh 'printenv >> Build_${BUILD_ID}_${STAGE_NAME}.log'
}

