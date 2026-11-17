# Ponto Falante — Secure DevOps & Cloud Computing

> **Estado do material:** MVP publicado no AWS Lightsail e validado em HTTPS. Imagem publicada no GHCR; pipeline CI aprovado com Gitleaks, Semgrep, build e Trivy. Deploy automático GitHub→AWS segue desativado porque a política do AWS Free plan bloqueia o provider OIDC necessário e a equipe não ativou plano pago. Métricas reais de CPU/memória foram coletadas; alarmes não são suportados pelo Lightsail Container Service. A API expõe previsões didáticas simuladas, sem conexão SPTrans.

## Ficha Técnica do MVP

- Produto: Ponto Falante — informação acessível sobre ônibus.
- Disciplina: Secure DevOps Tools & Cloud Computing (6 de 7), atividade Deploy Blindado.
- Integrantes e RMs:
  - Bryan Willian Messias Barbosa — RM 551305
  - Felipe Terra — RM 99405
  - Gabriel Doms — RM 98630
  - Lucas Vassão — RM 98607
  - Pedro Bicas — RM 99534
- URL publicada: https://ponto-falante.y48raqk9mz0k0.us-east-2.cs.amazonlightsail.com/
- Status validado em 17/11/2026: Lightsail `RUNNING`; `/health` retorna `ok`; `/api/status` informa `simulador`.
- Evidências da AWS: `docs/evidencias/aws-deploy-snapshot.json`. Plano Lightsail nano: preço de tabela US$ 7/mês, coberto pelos créditos do plano enquanto elegível; Cost Explorer ainda não refletia recurso criado hoje.
- Repositório público: https://github.com/FeTerra/GS-Secure-DevOps-Tools-Cloud-Computing
- Pipeline aprovado: https://github.com/FeTerra/GS-Secure-DevOps-Tools-Cloud-Computing/actions/runs/44000873548
- Execução anterior barrada pelo Trivy: https://github.com/FeTerra/GS-Secure-DevOps-Tools-Cloud-Computing/actions/runs/44000597597
- Stack: Python 3.12, FastAPI, Docker, Terraform (arquitetura EC2 de referência, não aplicada), AWS Lightsail Container Service, GitHub Actions, Gitleaks, Semgrep, Trivy, Prometheus e Grafana.
- Dados pessoais: nenhum coletado ou persistido nesta versão. Não há conta, nome, rosto, geolocalização, câmera nem histórico de passageiro.
- Dados de previsão: fixos e didáticos, sempre etiquetados `simulador`; não usar para deslocamento real.
- Responsabilidade compartilhada: equipe protege código, dependências e acesso ao GitHub; AWS protege a infraestrutura física e serviços gerenciados. HTTPS vem gerenciado pelo endpoint Lightsail; alertas de CPU/memória não são suportados para containers Lightsail.

## Rotas

- `GET /health` — verificação de saúde.
- `GET /api/status` — modo atual e aviso de simulação.
- `GET /api/pontos?busca=paulista` — ponto de demonstração.
- `GET /api/pontos/031245/previsoes` — previsões didáticas.
- `GET /metrics` — métricas Prometheus.

## Executar localmente

1. Instale Docker Desktop e Docker Compose v2.
2. Copie `.env.example` para `.env` e defina uma senha forte para Grafana. O arquivo `.env` não deve entrar no Git.
3. Rode `docker compose up --build -d`.
4. Abra `http://localhost:8000`, `http://localhost:3000` (Grafana) e `http://localhost:9090` (Prometheus). Interfaces de monitoramento ficam vinculadas somente a `127.0.0.1`.
5. Gere tráfego em `/health` e consulte o painel. Alertas estão definidos para indisponibilidade e p95 acima de 1 s por 5 min.
6. O `monitoring/prometheus.yml` já monitora o endpoint público HTTPS `/metrics` do Lightsail no job `ponto-falante`; o job `ponto-falante-local` existe para validar alertas de indisponibilidade de forma controlada sem parar a produção. O dashboard consulta somente o alvo público e mostra disponibilidade, req/s, erros HTTP e p95. No computador da equipe, Prometheus e Grafana foram executados nativamente porque Docker/WSL não estavam instalados; o snapshot com as leituras reais está em `docs/evidencias/monitoramento-publico.json`. Para execução com Compose, confira se a rede e os nomes dos serviços resolvem conforme o arquivo local.

## Pipeline DevSecOps

Em cada push e pull request, o workflow procura segredos com Gitleaks, executa regras Semgrep, constrói a imagem e interrompe o fluxo se Trivy encontrar vulnerabilidades HIGH/CRITICAL corrigíveis. No push para `main`, publica a imagem no GHCR. O deploy automático para AWS não foi habilitado: a política gerenciada da conta de projeto bloqueia a criação do provider IAM OIDC (`iam:*Provider*`) exigido pelo workflow; não foi ativado plano pago. A publicação atual no Lightsail foi manual com sessão temporária AWS, sem chave AWS persistente no GitHub. Não configure `DEPLOY_ENABLED=true` nessa conta. O pacote GHCR deve estar público para que a instância o baixe sem credenciais persistentes. Para cumprir a rubrica, registre um caso de segredo de teste barrado e a execução corrigida sem segredo real.

`terraform/` mantém a arquitetura EC2 de referência: VPC, subnet pública, rota/Internet Gateway, volume criptografado, IMDSv2 obrigatório e security group sem SSH. `terraform/lightsail-live/` descreve o container Lightsail publicado e tem instruções para importar os recursos existentes antes do `plan`; o state é local e nunca deve ser commitado. Apenas 80/443 entram. Os valores padrão apontam para a região `us-east-2`, a imagem deste repositório no GHCR e o repositório usado na confiança OIDC; podem ser sobrescritos com `terraform.tfvars` local não versionado. A arquitetura EC2/Terraform permanece como referência e não foi implantada nesta conta; o provider OIDC está bloqueado pela SCP gerenciada. `terraform.tfstate` pode conter dados sensíveis: mantenha fora do Git e restrinja permissões. Para produção, use state remoto criptografado com lock, TLS com domínio/certificado e alertas enviados a um canal operacional.

## Reproduzir infraestrutura

1. Configure credenciais AWS localmente pelo AWS CLI, nunca em arquivos versionados.
2. Em `terraform/`, crie `terraform.tfvars` com região e `image_uri` público do grupo.
3. A arquitetura EC2 do Terraform não foi aplicada nesta conta: a criação do provider OIDC está bloqueada pela política gerenciada AWS. Não execute `apply` nesta conta sem redesenhar a arquitetura e revisar o custo.
4. Para a implantação atual, acesse a URL Lightsail acima e valide `/health`; as respostas e métricas reais estão no JSON de evidências. O plano nano tem preço de tabela US$ 7/mês e permanece consumindo créditos enquanto ativo.
5. O Lightsail publicado permanece ativo e consome o plano nano (preço de tabela US$ 7/mês), coberto por créditos apenas enquanto elegível. Para encerrar, desative/exclua o serviço no console Lightsail após a avaliação; isso remove a URL pública. `terraform destroy` não encerra o serviço Lightsail.

## Evidências acadêmicas a anexar ao PDF

- Build do Compose e `docker compose ps` com serviços saudáveis.
- Dockerfile mostrando usuário não-root e ausência de segredos; saída do `docker inspect` sem privilégio root.
- Lightsail Container Service ativo, resposta de `/health`, métricas CPU/memória e custo de tabela/Cost Explorer no `docs/evidencias/aws-deploy-snapshot.json`. Não houve `terraform apply` nessa conta.
- GitHub Actions: execução anterior barrada na análise Trivy e execução corrigida com Gitleaks, Semgrep, Trivy e publicação GHCR aprovados (links na Ficha Técnica).
- URL publicada aberta e `/health` respondendo.
- Dashboard Prometheus/Grafana local apontado ao `/metrics` público do Lightsail, com quatro métricas e snapshot em `docs/evidencias/monitoramento-publico.json`. Capturas: `docs/evidencias/dashboard-grafana-publico.png` (quatro painéis reais) e `docs/evidencias/alerta-prometheus-firing.png` (`MVPIndisponivel` em FIRING). O alerta Prometheus local foi disparado em parada controlada de um probe local; não é alarme AWS, pois métricas do Lightsail Container Service não suportam alarmes.
- Custo real do Billing Calculator/Cost Explorer, região e período usados.

## Controles de segurança e limites

- Container como UID não-root, filesystem read-only, capabilities removidas, `no-new-privileges` e health check.
- Senhas locais via `.env`; segredos do deploy devem ficar em GitHub Secrets/OIDC, nunca na imagem, no Terraform state versionado ou no código.
- Nenhum dado pessoal é necessário ao MVP acadêmico. Logs não devem receber conteúdo de chat, imagem, identificador de veículo ou localização.
- O MVP atual usa HTTPS gerenciado pelo endpoint público do Lightsail. O exemplo alternativo EC2 do Terraform publica HTTP e abre 443 sem configurar TLS. Antes de uso real, conecte domínio próprio, revise segurança e custos.
- Prometheus/Grafana locais monitoram a URL publicada, mas seus próprios painéis não são publicados.

## Relatório e envio

O relatório e o PDF registram a URL pública Lightsail, limites do deploy automático, métricas observadas e custo real disponível na coleta. O alarme de container não existe nesse serviço e Cost Explorer pode atualizar com atraso. Confira as evidências e requisitos da rubrica antes do envio oficial. A disciplina exige PDF único com links clicáveis; o guia geral indica publicação e permanência do MVP por uma semana após 19/11.
