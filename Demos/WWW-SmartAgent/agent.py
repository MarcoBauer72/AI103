from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from functions import list_tables, describe_table, run_sql_query
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam


def main(): 
# 1. Conectar ao seu projeto do Azure AI Foundry
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(endpoint="https://projeto03-resource.services.ai.azure.com/api/projects/projeto03", credential=credential) as project_client,
        project_client.get_openai_client() as openai_client,
    ):    
        

    # 2. Empacotar as funções em ferramentas do Foundry
        sql_tools = FunctionTool(functions=[list_tables, describe_table, run_sql_query])

# 3. Criar o Agente de IA com as instruções do sistema
    agent = project_client.agents.create_version(
        agent_name="Agente-Analista-SQL",
        definition=PromptAgentDefinition(
        instructions=
            """Você é um analista de dados especialista em Azure SQL. 
            Sua tarefa é responder às perguntas do usuário consultando o banco de dados. 
            Siga estritamente este fluxo: 
            1. Chame 'list_tables' se não souber quais tabelas existem. 
            2. Chame 'describe_table' para entender o esquema das tabelas relevantes. 
            3. Formule uma query SQL precisa e execute-a com 'run_sql_query'. 
            4. Responda ao usuário de forma clara e resumida baseado nos dados retornados.""",
        tools=sql_tools,
        ),
    )


# Criar uma nova sessão/thread de conversa
    thread = project_client.agents.create_thread()

# Enviar uma pergunta que exige cruzar dados de várias tabelas
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="Quais foram as vendas de ontem considerando a tabela gold.fato_vendas_sku_n?"
    )

# Executar o agente na thread
    run = project_client.agents.create_run(thread_id=thread.id, agent_id=agent.id)

    # Processar as chamadas de ferramenta automáticas até o agente concluir a resposta
    while run.status in ["queued", "in_progress", "requires_action"]:
        # Se o modelo decidir que precisa rodar o SQL, o SDK gerencia a execução local da função
        if run.status == "requires_action":
            # O SDK do Foundry executa a função mapeada e devolve o resultado para o LLM
            run = project_client.agents.submit_tool_outputs_to_run(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=sql_tools.execute(run.required_action)
            )
        run = project_client.agents.get_run(thread_id=thread.id, run_id=run.id)

    # Exibir a resposta final estruturada
    messages = project_client.agents.list_messages(thread_id=thread.id)
    print(messages.text)

