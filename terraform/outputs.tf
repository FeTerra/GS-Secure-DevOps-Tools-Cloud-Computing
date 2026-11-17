output "public_url_http" {
  value = "http://${aws_instance.app.public_dns}"
}

output "instance_id" {
  value = aws_instance.app.id
}

output "github_deploy_role_arn" {
  value = aws_iam_role.github_deploy.arn
}
