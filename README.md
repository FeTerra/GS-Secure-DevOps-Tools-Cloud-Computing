# Ponto Falante — Secure DevOps & Cloud Computing

> **Estado do material:** repositório publicado e GitHub Actions concluído com Gitleaks, Semgrep, build e Trivy aprovados; a imagem foi publicada no GHCR. O deploy AWS, URL pública do MVP e capturas de monitoramento ainda dependem da conta da equipe. A tela reaproveitada é um protótipo visual; a API expõe previsões didáticas fixas e identificadas como simuladas. Não é integração com a SPTrans.

## Ficha Técnica do MVP

- Produto: Ponto Falante — informação acessível sobre ônibus.
- Disciplina: Secure DevOps Tools & Cloud Computing (6 de 7), atividade Deploy Blindado.
- Integrantes e RMs:
  - Bryan Willian Messias Barbosa — RM 551305
  - Felipe Terra — RM 99405
  - Gabriel Doms — RM 98630
  - Lucas Vassão — RM 98607
  - Pedro Bicas — RM 99534
- URL publicada: **PENDENTE após provisionamento**.
- Repositório público: https://github.com/FeTerra/GS-Secure-DevOps-Tools-Cloud-Computing
- Pipeline aprovado: https://github.com/FeTerra/GS-Secure-DevOps-Tools-Cloud-Computing/actions/runs/44000873548
- Execução anterior barrada pelo Trivy: https://github.com/FeTerra/GS-Secure-DevOps-Tools-Cloud-Computing/actions/runs/44000597597
- Stack: Python 3.12, FastAPI, Docker, Terraform, AWS EC2, GitHub Actions, Gitleaks, Semgrep, Trivy, Prometheus e Grafana.
- Dados pessoais: nenhum coletado ou persistido nesta versão. Não há conta, nome, rosto, geolocalização, câmera nem histórico de passageiro.
- Dados de previsão: fixos e didáticos, sempre etiquetados `simulador`; não usar para deslocamento real.
- Responsabilidade compartilhada: equipe protege código, dependências, variáveis e acesso ao GitHub; AWS protege a infraestrutura física e os serviços gerenciados; equipe ainda precisa configurar domínio/TLS e monitoramento de produção.

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
6. Para monitorar o MVP publicado, ajuste `monitoring/prometheus.yml`: troque o alvo `app:8000` pelo DNS público da instância com a porta `80`. Mantenha Prometheus e Grafana locais e não abra as portas `9090`/`3000` na nuvem.

## Pipeline DevSecOps

Em cada push e pull request, o workflow procura segredos com Gitleaks, executa regras Semgrep, constrói a imagem e interrompe o fluxo se Trivy encontrar vulnerabilidades HIGH/CRITICAL corrigíveis. No push para `main`, publica a imagem no GHCR. Após o bootstrap da EC2, o mesmo workflow assume uma role temporária via OIDC e atualiza o container pelo SSM. Configure o secret `AWS_DEPLOY_ROLE_ARN`, as variáveis `AWS_REGION`, `EC2_INSTANCE_ID` e `DEPLOY_ENABLED=true`. O pacote GHCR deve estar público para que a instância o baixe sem credenciais persistentes. Para cumprir a rubrica, registre um caso de segredo de teste barrado e a execução corrigida sem segredo real.

`terraform/` cria VPC, subnet pública, rota/Internet Gateway, EC2 com volume criptografado, IMDSv2 obrigatório e security group sem SSH. Apenas 80/443 entram. Configure valores com `terraform.tfvars` local não versionado; substitua a imagem GHCR e `github_repository`. O apply retorna `github_deploy_role_arn` e `instance_id` para configurar no GitHub. O apply também registra o provedor OIDC; se ele já existir na conta, importe/adote o recurso no state antes de aplicar. `terraform.tfstate` pode conter dados sensíveis: mantenha fora do Git e restrinja permissões. Para produção, use state remoto criptografado com lock, TLS com domínio/certificado e alertas enviados a um canal operacional.

## Reproduzir infraestrutura

1. Configure credenciais AWS localmente pelo AWS CLI, nunca em arquivos versionados.
2. Em `terraform/`, crie `terraform.tfvars` com região e `image_uri` público do grupo.
3. Execute `terraform init`, `terraform plan` e revise recursos/custos; depois `terraform apply`.
4. Aguarde o user-data concluir, valide `/health` na URL retornada e registre a captura do painel AWS e do MVP.
5. Após a avaliação, rode `terraform destroy` para evitar cobrança contínua.

## Evidências acadêmicas a anexar ao PDF

- Build do Compose e `docker compose ps` com serviços saudáveis.
- Dockerfile mostrando usuário não-root e ausência de segredos; saída do `docker inspect` sem privilégio root.
- Terraform plan/apply, console com instância e regra sem SSH/porta administrativa.
- GitHub Actions: execução anterior barrada na análise Trivy e execução corrigida com Gitleaks, Semgrep, Trivy e publicação GHCR aprovados (links na Ficha Técnica).
- URL publicada aberta e `/health` respondendo.
- Dashboard com tráfego, taxa de erro, latência p95 e disponibilidade; alerta realmente disparado.
- Custo real do Billing Calculator/Cost Explorer, região e período usados.

## Controles de segurança e limites

- Container como UID não-root, filesystem read-only, capabilities removidas, `no-new-privileges` e health check.
- Senhas locais via `.env`; segredos do deploy devem ficar em GitHub Secrets/OIDC, nunca na imagem, no Terraform state versionado ou no código.
- Nenhum dado pessoal é necessário ao MVP acadêmico. Logs não devem receber conteúdo de chat, imagem, identificador de veículo ou localização.
- O exemplo cloud publica HTTP na porta 80 e abre 443 sem configurar TLS. Trate-o como demonstração; antes de uso real, conecte domínio e TLS, restrinja exposição e valide segurança/custo.
- Prometheus/Grafana locais monitoram a URL publicada, mas seus próprios painéis não são publicados.

## Relatório e envio

O relatório está em `docs/relatorio-devops.md` e o PDF preparado em `docs/DevOps_Ponto_Falante.pdf`. A identificação, link do repositório e evidências de pipeline foram preenchidos; a URL pública do MVP, infraestrutura publicada e capturas de dashboard/alerta/custo ainda precisam ser adicionadas antes do envio oficial. A disciplina exige PDF único com links clicáveis; o guia geral indica publicação e permanência do MVP por uma semana após 19/11.
