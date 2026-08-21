import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o cliente para apontar para o LM Studio local
client = OpenAI(
    base_url = os.getenv("LMSTUDIO_BASE_URL"),  
    api_key = os.getenv("LMSTUDIO_API_KEY")
)
# Track responses
last_response_id = None

while True:
    entrada = input("Em que posso ajudar hoje? (* digite ""sair"" para encerrar o chat): ")

    # Verifica se o usuário digitou a palavra sair (convertida para minúsculas)
    if entrada.lower().strip() == 'sair':
        print("Encerrando o chat. Até logo!")
        break
        
    payload = {
        "message": f"{entrada}",
        "role": "user"
    }

    try:
        # Envia a mensagem para o modelo local
        response = client.responses.create(
                    model=os.getenv("LMSTUDIO_MODEL"),
                    instructions="Seja um assistente útil e direto e sempre responda exclusivamente na língua Portugues do Brasil.",
                    input=entrada,
                    previous_response_id=last_response_id,
        )

        last_response_id = response.id     
        
        # Exibe a resposta do LLM
        print(response.output_text)

    except requests.exceptions.ConnectionError:
        print(
            "O LLM local não está em execução. Por favor, inicie o servidor local e tente novamente."
        )