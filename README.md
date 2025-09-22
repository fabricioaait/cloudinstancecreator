# Cloud Provider Application

Aplicação modular em Python para criar e deletar instâncias em AWS e Azure.

## Funcionalidades
- Interface CloudProvider com métodos create_instance e delete_instance.
- Implementações para AWS (usando boto3) e Azure (simulado).
- Fábrica para seleção baseada em config.yaml.
- Princípios SOLID e DRY aplicados.
- Limitação a 1 instância por execução, tamanho mínimo (t2.micro para AWS, Standard_B1s para Azure).

## Configuração
1. Instale dependências: `pip install -r requirements.txt`
2. Configure config.yaml:
   ```yaml
   provider: aws  # ou azure
   quantity: 1    # sempre 1
   size: t2.micro # ou Standard_B1s
   ```
3. Para AWS: Defina variáveis de ambiente AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION.
4. Para Azure: AZURE_CLIENT_ID, etc. (mas atualmente simulado).

## Políticas IAM
- AWS: Use aws-iam-policy.json para criar política com permissões mínimas para t2.micro e MaxCount=1.
- Azure: Use azure-custom-role.json para role custom (limitação de tamanho e quantidade via código).

## GitHub Actions
- Workflow roda em PR approved.
- Configure secrets no repositório: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, etc.
- Para Azure, adicione AZURE_* secrets.

## Testes
Execute `pytest` para rodar testes unitários.