import os
import json
from dotenv import load_dotenv

# Add references
# Add references
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition, FunctionTool
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam
from functions import list_tables, describe_table, run_sql_query

def main(): 
    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')

    # Load environment variables from .env file
    load_dotenv()
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT_NAME")

    # Connect to the project client
    # Connect to the project client
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):    

        # Define the event function tool
        # Define the event function tool
        # lista_tabelas = FunctionTool(
        #     name="list_tables",
        #     description="List all tables in the database.",
        #     parameters={
        #         "type": "object",
        #         "properties": {},
        #         "additionalProperties": False,
        #     },
        #     strict=True,
        # )        

        # descreve_tabela = FunctionTool(
        #     name="describe_table",
        #     description="Describe the columns and data types of a specific table.",
        #     parameters={
        #         "type": "object",
        #         "properties": {
        #             "table_name": {
        #                 "type": "string",
        #                 "description": "The name of the table to describe."
        #             }
        #         },
        #         "required": ["table_name"],
        #         "additionalProperties": False,
        #     },
        #     strict=True,
        # )             
          

        consulta_tabela = FunctionTool(
            name="run_sql_query",
            description="Execute a SQL query and return the results.",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute."
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
            strict=True,
        )    

        # Create a new agent with the function tools
        # Create a new agent with the function tools
        agent = project_client.agents.create_version(
            agent_name="Agente-Analista-SQL",
            definition=PromptAgentDefinition(
                model=model_deployment,
                instructions=
                """Você é um analista de dados especialista em Azure SQL. 
                    Sua tarefa é responder às perguntas do usuário consultando o banco de dados. 
                    Siga estritamente este fluxo: 
                    1. Formule uma query SQL precisa e execute-a com 'run_sql_query'. 
                    2. Formule uma query SQL sobre vendas consulte a tabela gold.fato_vendas_sku_n
                    3. Formule uma query SQL sobre estoque consulte a tabela gold.fato_estoq_w_sku_n""",
                #tools=[lista_tabelas, descreve_tabela, consulta_tabela],
                tools=[consulta_tabela],
            ),
        )        
        
        # Create a thread for the chat session
        # Create a thread for the chat session
        conversation = openai_client.conversations.create()        

        # Create a list to hold function call outputs that will be sent back as input to the agent
        # Create a list to hold function call outputs that will be sent back as input to the agent
        input_list: ResponseInputParam = []        
        
        while True:
            user_input = input("Enter the table name or 'list' to see all tables. Use 'quit' to exit.\nUSER: ").strip()
            if user_input.lower() == "quit":
                print("Exiting chat.")
                break

            # Send a prompt to the agent
            # Send a prompt to the agent
            openai_client.conversations.items.create(
                conversation_id=conversation.id,
                items=[{"type": "message", "role": "user", "content": user_input}],
            )           
                    
            # Retrieve the agent's response, which may include function calls
            # Retrieve the agent's response, which may include function calls
            response = openai_client.responses.create(
                conversation=conversation.id,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                input=input_list,
            )

            # Check the run status for failures
            if response.status == "failed":
                print(f"Response failed: {response.error}")

            # Process function calls
            # Process function calls
            for item in response.output:
                if item.type == "function_call":
                    # Retrieve the matching function tool
                    function_name = item.name
                    result = None
                    if item.name == "run_sql_query":
                        result = run_sql_query(**json.loads(item.arguments))
                    # Append the output text
                    input_list.append(
                        FunctionCallOutput(
                            type="function_call_output",
                            call_id=item.call_id,
                            output=result,
                        )
                    )            

            # Send function call outputs back to the model and retrieve a response
            # Send function call outputs back to the model and retrieve a response
            if input_list:
                response = openai_client.responses.create(
                    input=input_list,
                    previous_response_id=response.id,
                    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
                )
            # Display the agent's response
            print(f"AGENT: {response.output_text}")            

        # Delete the agent when done
        # Delete the agent when done
        # project_client.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
        # print("Deleted agent.")        

if __name__ == '__main__': 
    main()