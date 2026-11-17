terraform {
  required_version = ">= 1.7.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region containing the already-running Lightsail service."
  type        = string
  default     = "us-east-2"
}

resource "aws_lightsail_container_service" "ponto_falante" {
  name        = "ponto-falante"
  power       = "nano"
  scale       = 1
  is_disabled = false
  tags        = { Project = "GlobalSolution" }
}

resource "aws_lightsail_container_service_deployment_version" "ponto_falante" {
  service_name = aws_lightsail_container_service.ponto_falante.name

  container {
    container_name = "ponto-falante"
    image          = "ghcr.io/feterra/gs-secure-devops-tools-cloud-computing:latest"
    command        = []
    environment    = {}
    ports          = { "8000" = "HTTP" }
  }

  public_endpoint {
    container_name = "ponto-falante"
    container_port = 8000

    health_check {
      healthy_threshold   = 2
      unhealthy_threshold = 2
      timeout_seconds     = 5
      interval_seconds    = 30
      path                = "/health"
      success_codes       = "200-299"
    }
  }
}

output "service_url" {
  description = "Public HTTPS endpoint assigned by Lightsail."
  value       = aws_lightsail_container_service.ponto_falante.url
}
