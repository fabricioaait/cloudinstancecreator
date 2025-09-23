# Cloud Instance Creator

## Descrição do Programa
Aplicação Python modular que lê config.yaml para selecionar provedor (AWS/Azure), cria/deleta instâncias via interface CloudProvider.

### 1. Aplicação Modular Orientada a Objetos
- Interface CloudProvider (src/cloud_provider.py, linhas 10-20) com create_instance() e delete_instance().
- Implementações: AWSProvider (src/aws_provider.py) e AzureProvider (src/azure_provider.py).
- Fábrica: get_provider() em src/factory.py (linha 5) seleciona baseado em config['provider'].

### 2. Princípios SOLID e DRY
- **S (Single Responsibility)**: CloudProvider define interface (src/cloud_provider.py); AWSProvider gerencia EC2 (src/aws_provider.py); Main orquestra (main.py, linhas 5-30).
- **O (Open/Closed)**: Novos provedores via subclasse de CloudProvider sem modificar código existente.
- **L (Liskov Substitution)**: AWSProvider/AzureProvider substituem CloudProvider (src/aws_provider.py linha 5, src/azure_provider.py linha 5).
- **I (Interface Segregation)**: CloudProvider mínima, focada em instâncias (src/cloud_provider.py).
- **D (Dependency Inversion)**: Main depende de CloudProvider, não concretos (main.py linha 7).
- **DRY**: Lógica compartilhada via interface; config evita repetição (config.yaml para múltiplos grupos).

## Métodos de Criação e Delete
- **Criação**: create_instance(instance_type, name) - AWS: boto3 run_instances (src/aws_provider.py linha 15); Azure: simulado (src/azure_provider.py linha 10).
- **Delete**: delete_instance(instance_id) - AWS: boto3 terminate_instances (src/aws_provider.py linha 25); Azure: simulado (src/azure_provider.py linha 15).

## Configuração
1. `pip install -r requirements.txt`
2. Edite config.yaml com instance_groups.
3. Vars env: AWS_* e AZURE_*.

## Políticas IAM
- AWS: aws-iam-policy.json.
- Azure: azure-custom-role.json.

## GitHub Actions
- Workflow em .github/workflows/ci.yml roda em push main com config.yaml.

## Testes
`pytest` para testes unitários.
