#!groovy
def props
def getEnv(branch) {
    return (branch == 'master') ? 'prod' : (branch == 'develop') ? 'dev' : 'local'
}

def getPort(env) {
    return (APP_ENV == 'dev') ? '3080' : (APP_ENV == 'prod') ? '4080' : '2080'
}

def bucketEnv(env) {
    return (APP_ENV == 'dev') ? '3080' : (APP_ENV == 'prod') ? '4080' : '2080'
}
def getDatabaseURL(branch) {
    return (
        (APP_ENV == 'dev')
             ? 'mysqlgis://sernatur_c19trace_dev:rFJMLKMAXa3Qj8zbcaTdGmaNMgTsMTunTTgwBCRTat8LcKSZub3ERxdBHvndDryD@172.17.0.1/sernatur_c19trace_dev'
             : (
                 (APP_ENV == 'prod')
                     ? 'mysqlgis://sernatur_c19trace_prod:rFJMLKMAXa3Qj8zbcaTdGmaNMgTsMTunTTgwBCRTat8LcKSZub3ERxdBHvndDryD@172.17.0.1/sernatur_c19trace_prod'
                     : 'mysqlgis://sernatur_c19trace_local:Ev4f5cQwYPYfXLu4FxwrQehsrvx3Mt76dbQ8y5RWGDuG7pJzqWsGSjf6rUvQnu64@172.17.0.1/sernatur_c19trace_local'
            )
    )
}

pipeline {
  agent {label 'linux'}
  environment {
    GIT_USER  = sh (script: 'git --no-pager show -s --format=\'%ae\'', returnStdout: true).trim()
    APP_ENV = getEnv(env.branch_NAME)
    registry = "docker.pkg.github.com/apareja1/sernatur-backend"
    pkgName = "sernatur-backend"
    registryCred = "GH_TOKEN"
    CONFIG_GENERIC = "c807b08f-f27f-44de-8181-037708ece077"
  }
  triggers {
    githubPush()
  }
  stages {
    stage ('Checkout'){
      steps{
        echo 'Pulling...' + env.branch_NAME
        checkout scm
      }
    }

//    stage ('Static'){
//      environment {
//        DJANGO_SETTINGS_MODULE="settings.env.${APP_ENV}"
//        DATABASE_DEFAULT_URL="sqlite:///:memory:"
//      }
//      when {
//      expression { env.BRANCH_NAME ==~ /^feature\/[a-zA-Z\d_-]+$/ || env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'master' }
//      }
//      steps{
//        script{
//          sh "export"
//          sh "python -m venv .venv"
//          sh "source .venv/bin/activate; xargs -n 1 pip install < requirements.txt || true";
//          sh "source .venv/bin/activate; pip install gdal==$(gdal-config --version)"
//          sh "source .venv/bin/activate; python manage.py collectstatic"
//        }
//      }
//    }

    stage ('Docker build and Push2GH') {
      steps{
        script{
          sh "export"
          def dockerImage = docker.build("${registry}/${pkgName}:${env.GIT_COMMIT}", "-f Dockerfile ./")
          docker.withRegistry('https://'+registry, registryCred) {
            dockerImage.push("${env.GIT_COMMIT}")
            dockerImage.push("latest")
          }
        }
      }
    }

    stage ('Deploy') {
      agent {label 'host-to-deploy'}
      environment {
        PORT_ENV = getPort(APP_ENV)
        DATABASE_DEFAULT_URL = getDatabaseURL(APP_ENV)
      }
      when {
      expression { env.BRANCH_NAME ==~ /^feature\/[a-zA-Z\d_-]+$/ || env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'master' }
      }
      steps{
        script{
          configFileProvider(
            [configFile(fileId: "${CONFIG_GENERIC}", variable: 'configFile')]) {
              props = readProperties file: "$configFile"
            }
            env.MAIL_S3_BUCKET_NAME = props['_MAIL_S3_BUCKET_NAME']
            env.MAIL_STATIC_BASE    = 'https://'+MAIL_S3_BUCKET_NAME+props['_MAIL_STATIC_BASE']
            env.MAIL_FROM           = props['_MAIL_FROM']
            env.deployImage = "${registry}/${pkgName}:${env.GIT_COMMIT}"
            echo "Deploy image en ${APP_ENV}"
            docker.withRegistry('https://'+registry, registryCred) {
              withCredentials([usernamePassword(credentialsId: 'aws-dev-sernatur', passwordVariable: 'AWS_KEY', usernameVariable: 'AWS_ID')]) {
                sh '''
                #!/bin/bash
                set +x
                runFocker () {
                  docker run -itd --name ${pkgName}-${APP_ENV}\
                  -e "DJANGO_SETTINGS_MODULE=settings.env.${APP_ENV}"\
                  -e "DATABASE_DEFAULT_URL=${DATABASE_DEFAULT_URL}"\
                  -e "MAIL_FROM=${MAIL_FROM}"\
                  -e "MAIL_STATIC_BASE=${MAIL_STATIC_BASE}"\
                  -e "MAIL_S3_BUCKET_NAME=${MAIL_S3_BUCKET_NAME}"\
                  -e "MAIL_S3_BUCKET_AWS_ACCESS_KEY_ID=${AWS_ID}"\
                  -e "MAIL_S3_BUCKET_AWS_SECRET_ACCESS_KEY=${AWS_KEY}"\
                  -e "AWS_SES_ACCESS_KEY_ID=${AWS_ID}"\
                  -e "AWS_SES_SECRET_ACCESS_KEY=${AWS_KEY}"\
                  --restart always -p ${PORT_ENV}:80 ${deployImage};
                }
                issue=$(docker ps -a | grep ${pkgName}-${APP_ENV}| awk '{print $1}')
                if [ -z "$issue" ];
                then
                echo "Nuevo despliegue"
                runFocker
                else
                echo "Actualiza Docker"
                docker stop ${pkgName}-${APP_ENV} && docker rm ${pkgName}-${APP_ENV}
                echo "Run ${deployImage}"
                runFocker
                fi
                sleep 5
                echo ""
                echo "### Healthy Docker Image ###"
                docker ps -a --format "{{.Names}}: {{.Status}} {{.ID}}" --filter "name=${pkgName}-${APP_ENV}"
                echo "----------------------------"
                echo ""
                '''
              }
            }
          }
        }
      }
  //Stages
  }
  post {
    success {
      sh 'echo Sucesss Pipeline!!'
         slackSend channel: '#dev',
                   color: 'good',
                   message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n by ${env.GIT_USER}\n Info at: ${env.BUILD_URL}"
    }
    unstable {
      sh 'echo Unsucessful Pipeline!!'
         slackSend channel: '#dev',
                  color: 'warning',
                   message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n by ${env.GIT_USER}\n Info at: ${env.BUILD_URL}"
    }
    failure {
      sh 'echo Failure Pipeline!!'
         slackSend channel: '#dev',
                  color: 'danger',
                   message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n by ${env.GIT_USER}\n Info at: ${env.BUILD_URL}"

    }
    aborted {
      sh 'echo aborted Pipeline!!'
         slackSend channel: '#dev',
                  color: 'danger',
                   message: "*${currentBuild.currentResult}:* Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n by ${env.GIT_USER}\n Info at: ${env.BUILD_URL}"
    }
    always {
      echo 'Limpiando espacio de trabajo....'
      cleanWs()
    }
  }
}
