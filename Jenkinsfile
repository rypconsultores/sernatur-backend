#!groovy
def props
def getEnv(branch) {
  return (branch == 'master') ? 'prod' : (branch == 'develop') ? 'cert' : 'dev'
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

    stage ('Deploy k8') {
      environment {
        dockerImageDeploy = "${registry}/${pkgName}:${env.GIT_COMMIT}"
      }
      when {
        expression { env.BRANCH_NAME ==~ /^feature\/[a-zA-Z\d_-]+$/ || env.BRANCH_NAME == 'develop' || env.BRANCH_NAME == 'master' }
      }
      steps {
        script {
          if ( env.BRANCH_NAME ==~ /^feature\/[a-zA-Z\d_-]+$/ ){
            withKubeConfig([credentialsId: 'kubeconfig-dev']) {
              sh '''
              kubectl set image deployment/${pkgName} ${pkgName}-container=${dockerImageDeploy} -n desarrollo
              '''
            }
          }
          if ( env.BRANCH_NAME == 'develop' ){
            withKubeConfig([credentialsId: 'kubeconfig-cert']) {
              sh '''
              kubectl set image deployment/${pkgName} ${pkgName}-container=${dockerImageDeploy} -n certificacion
              '''
            }
          }
          if ( env.BRANCH_NAME == 'master' ){
            withKubeConfig([credentialsId: 'kubeconfig']) {
              sh '''
              kubectl set image deployment/${pkgName} ${pkgName}-container=${dockerImageDeploy} -n produccion
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
