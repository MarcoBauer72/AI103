import os
import requests
import json
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

BASE_URL = os.getenv("ANYTHINGLLM_BASE_URL")
API_KEY = os.getenv("ANYTHINGLLM_API_KEY")
WORKSPACE_SLUG = os.getenv("ANYTHINGLLM_WORKSPACE_SLUG")

url = f"{BASE_URL}/workspace/{WORKSPACE_SLUG}/chat"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

while True:
    entrada = input("Em que posso ajudar hoje? (* digite ""sair"" para encerrar o chat): ")

    # Verifica se o usuário digitou a palavra sair (convertida para minúsculas)
    if entrada.lower().strip() == 'sair':
        print("Encerrando o chat. Até logo!")
        break
        
    payload = {
        "message": f"{entrada}",
        "mode": "chat"
    }

    try:
        # 5. Send the POST request to your local server
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        # 6. Parse and display the response
        if response.status_code == 200:
            response_data = response.json()
            # AnythingLLM returns the message inside the 'textResponse' key
            ai_response = response_data.get("textResponse", "Nenhuma resposta encontrada.")
            print(f"AI Response:\n{ai_response}")
        else:
            print(f"Error {response.status_code}: {response.text}")

    except requests.exceptions.ConnectionError:
        print(
            "O LLM local não está em execução. Por favor, inicie o servidor local e tente novamente."
        )