variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "image_uri" {
  description = "Imagem pública publicada no GHCR; altere pelo nome do seu repositório."
  type        = string
  default     = "ghcr.io/SEU-USUARIO/ponto-falante:latest"
}

variable "github_repository" {
  description = "owner/repo exato usado no sub do OIDC GitHub."
  type        = string
  default     = "SEU-USUARIO/ponto-falante"
}
