# Cloud Instance Creator

Aplicação modular orientada a objetos em Python para criar e deletar instâncias de máquinas virtuais em provedores de nuvem AWS e Azure, baseada em configuração YAML.

## Descrição do Programa
O programa lê um arquivo `config.yaml` com grupos de instâncias, cada um especificando provedor (AWS ou Azure), tamanho, quantidade, etc. Utiliza uma fábrica para instanciar o provedor correto, cria as instâncias via API do provedor, e opcionalmente as deleta (com flag `cleanup`).

## Respostas ao Exercício

### 1. Aplicação Modular Orientada a Objetos
- **Interface CloudProvider**: Definida em `src/cloud_provider.py` com métodos abstratos `create_instance(instance_type, name)` e `delete_instance(instance_id)`.
- **Implementações**:
  - `AWSProvider` (`src/aws_provider.py`): Usa boto3 para criar/deletar EC2 instances reais.
  - `AzureProvider` (`src/azure_provider.py`): Simulado (imprime ações; pode ser implementado com Azure SDK).
- **Fábrica**: `src/factory.py` com função `get_provider(config)` que retorna instância do provedor baseado em `config['provider']`.
- **Configuração YAML**: `config.yaml` define `instance_groups` com provedor, tamanho, quantidade, etc.

### 2. Princípios SOLID e DRY
- **S (Single Responsibility)**: Cada classe tem responsabilidade única.
  - `CloudProvider`: Define interface para provedores.
  - `AWSProvider`: Gerencia EC2 via boto3.
  - `AzureProvider`: Gerencia Azure (simulado).
  - `Factory`: Cria instâncias de provedores.
  - `Main`: Orquestra leitura de config, criação/deleção.
- **O (Open/Closed)**: Aberto para extensão (adicionar novos provedores implementando CloudProvider), fechado para modificação (não alterar código existente).
- **L (Liskov Substitution)**: Subclasses `AWSProvider` e `AzureProvider` podem substituir `CloudProvider` sem quebrar funcionalidade.
- **I (Interface Segregation)**: Interface `CloudProvider` é mínima e focada em criação/deleção de instâncias.
- **D (Dependency Inversion)**: Código depende de abstração `CloudProvider`, não de concretos (AWS/Azure).
- **DRY (Don't Repeat Yourself)**: Lógica de criação/deleção é compartilhada via interface; configuração evita duplicação de código para diferentes grupos.

## Funcionalidades
- Criação e deleção de instâncias baseada em config YAML.
- Suporte a múltiplos grupos por execução.
- Flag `cleanup` por grupo para manter instâncias.
- Limitação de quantidade (0-5) e tamanhos específicos para segurança.

## Configuração
1. Instale dependências: `pip install -r requirements.txt`
2. Edite `config.yaml`:
   ```yaml
   instance_groups:
     prod:
       provider: aws
       size: t3.micro
       ami: ami-0c02fb55956c7d316
       name_pattern: "prod-instance-{number}"
       quantity: 1
       cleanup: false  # Opcional: true para deletar após criação
   ```
3. Variáveis de ambiente:
   - AWS: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
   - Azure: AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID, AZURE_RESOURCE_GROUP, AZURE_LOCATION

## Políticas IAM
- AWS: `aws-iam-policy.json` com permissões para EC2 (RunInstances, etc.).
- Azure: `azure-custom-role.json` para role custom.

## GitHub Actions
- Workflow em `.github/workflows/ci.yml` roda em push para main com mudanças em `config.yaml`.
- Secrets: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AZURE_*.

## Testes
Execute `pytest` para testes unitários (mocks para AWS, simulação para Azure).