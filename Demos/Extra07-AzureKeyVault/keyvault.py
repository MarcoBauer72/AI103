import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# az login --tenant "3d3dcbf1-320a-4606-9a6f-bc3eed112148"
# escolher a assinatura : 95d2faa5-b447-4285-a193-6f88eed31463

keyVaultName = "azkeyvaultbauerka"
KVUri = f"https://{keyVaultName}.vault.azure.net"

credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

secretName = "senhadobauer"

print(f"Retrieving your secret from KV_NAME.")

retrieved_secret = client.get_secret(secretName)

print(f"Your secret is '{retrieved_secret.value}'.")