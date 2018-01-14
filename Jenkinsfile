#!/usr/bin/env groovy

def installBuildRequirements(){
  // Disabled in pipeline. Those commands need to be installed as user root.
	echo "[DISABLED] sudo npm install -g typescript"
	echo "[DISABLED] sudo npm install -g vsce"
}

def buildVscodeExtension(){
	sh "npm install"
	sh "npm run vscode:prepublish"
}

node {
	stage 'Checkout code'
	deleteDir()
	git url: 'https://github.com/korekontrol/vscode-saltstack.git'

	stage 'Install build requirements'
	installBuildRequirements()

	stage 'Build'
	sh "npm install"
	sh "npm run vscode:prepublish"

	stage "Package"
	def packageJson = readJSON file: 'package.json'
	sh "vsce package -o saltstack-${packageJson.version}-${env.BUILD_NUMBER}.vsix"

	stage 'Stash'
	def vsix = findFiles(glob: '**.vsix')
	stash name:'vsix', includes:vsix[0].path
}

node {
	timeout(time:7, unit:'DAYS') {
		input message:'Approve deployment?', submitter: 'elephant'
	}

	stage "Publish to Marketplace"
	unstash 'vsix';
	withCredentials([[$class: 'StringBinding', credentialsId: 'vscode_marketplace', variable: 'TOKEN']]) {
		def vsix = findFiles(glob: '**.vsix')
		sh 'vsce publish -p ${TOKEN} --packagePath' + " ${vsix[0].path}"
	}
	archive includes:"**.vsix"
}