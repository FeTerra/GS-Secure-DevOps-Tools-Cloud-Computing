# Lightsail publicado sob Terraform

Este módulo descreve o serviço `ponto-falante` e sua versão de deployment atual. O código foi acrescentado após a criação manual inicial do serviço. Para adotar o recurso existente sem recriá-lo, inicialize o provider e importe o service e deployment antes de qualquer `apply`:

```powershell
$env:AWS_PROFILE = "MakeItHappen"
$env:AWS_REGION = "us-east-2"
terraform init
terraform import aws_lightsail_container_service.ponto_falante ponto-falante
terraform import aws_lightsail_container_service_deployment_version.ponto_falante ponto-falante/1
terraform plan
```

Revise o plano; não aplique caso ele proponha substituir/desativar o service ou mudar o deployment sem intenção. `terraform.tfstate` contém dados da conta e fica local, ignorado pelo Git. O URL público é exportado como `service_url`.

O power `nano` custa US$ 7/mês pelo preço de tabela. A aplicação usa imagem GHCR pública; esta automação do módulo não depende de OIDC. O workflow GitHub Actions de deploy AWS continua desativado porque a conta de projeto bloqueia a criação do provider IAM OIDC; este código não cria credenciais persistentes.
