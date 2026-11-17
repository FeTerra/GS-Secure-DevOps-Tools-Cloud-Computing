variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "image_uri" {
  description = "Imagem publicada no GHCR pelo workflow deste repositório."
  type        = string
  default     = "ghcr.io/feterra/gs-secure-devops-tools-cloud-computing:latest"
}

variable "github_repository" {
  description = "owner/repo exato usado no sub do OIDC GitHub."
  type        = string
  default     = "FeTerra/GS-Secure-DevOps-Tools-Cloud-Computing"
}
