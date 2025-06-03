pipeline
{
agent any
stages
{
stage('Start')
{
steps
{
echo 'Start Lab_7'
}
}
stage('Auth to HCP')
{
steps
{
withCredentials([usernamePassword(credentialsId: 'hcp',
usernameVariable: 'MY_ID', passwordVariable: 'MY_SECRET')])
{
script
{
sh 'hcp auth login --client-id $MY_ID --client-secret
$MY_SECRET'
}
}
}
}stage('Init HCP')
{
steps
{
sh 'hcp profile set vault-secrets/app lab-7'
}
}
stage('Build nginx/custom')
{
steps
{
sh 'docker build -t nginx/custom:latest .'
}
}
stage('Deploy nginx/custom')
{
steps
{
sh 'docker run -d -p 80:80 nginx/custom:latest'
}
}
stage('Finish')
{
steps
{
echo 'Finish Lab_7'
}
}
}
post
{
always
{
script
{
env.webhookUrl = sh(script: 'hcp vault-secrets secrets open
teams_microsoft_webhook --format=json | jq -r .static_version.value', returnStdout:
true).trim()
}
}
success
{
office365ConnectorSend(
webhookUrl: webhookUrl,
message: "✅ Build success!",
status: "Success",
color: "00FF00"
)
}failure
{
office365ConnectorSend(
webhookUrl: webhookUrl,
message: "❌ Build failed!",
status: "Failure",
color: "FF0000"
)
}
}
}
