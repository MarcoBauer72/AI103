import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER").strip()
SQL_DATABASE = os.getenv("SQL_DATABASE").strip()
SQL_DRIVER = os.getenv("SQL_DRIVER").strip()
UID = os.getenv("SQL_USER").strip()
PWD = os.getenv("SQL_PASSWORD").strip()

# Defina a sua string de conexão segura
CONN_STR = (
    f"Driver={SQL_DRIVER};"
    f"Server=tcp:{SQL_SERVER},1433;"
    f"Database={SQL_DATABASE};"
    f"Encrypt=no;"
    f"UID={UID};"
    f"PWD={PWD};"
    f"Connection Timeout=30;"
)

def list_tables() -> str:
    """Lista todas as tabelas disponíveis no banco de dados para o agente saber onde procurar."""
    with pyodbc.connect(CONN_STR) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'")
        tables = [row[0] for row in cursor.fetchall()]
    return f"Tabelas disponíveis: {', '.join(tables)}"

def describe_table(table_name: str) -> str:
    """Retorna as colunas e tipos de uma tabela específica para o agente montar a query certa."""
    with pyodbc.connect(CONN_STR) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'")
        columns = [f"{row[0]} ({row[1]})" for row in cursor.fetchall()]
    return f"Colunas da tabela {table_name}: {', '.join(columns)}"

def run_sql_query(query: str) -> str:
    """Executa de forma segura uma query SQL gerada pelo agente e retorna os dados em string.
    Para perguntas sobre VENDAS consulta a tabela SQL chamada fato_vendas_sku_n.
    Na tabela gold.fato_vendas_sku_n a coluna qty_sales representa a quantidade vendida e a coluna vlr_sales
    representa o valor total da venda.
    Para perguntas sobre ESTOQUE consulte a tabela SQL chamada gold.fato_estoq_w_sku_n.
    Consulte apenas as tabelas "gold.fato_estoq_w_sku_n" ou a tabela "gold.fato_vendas_sku_n"
    Por exemplo, para perguntas sobre vendas, o agente deve gerar uma query do tipo:
    SELECT SUM(qty_sales) AS total_qty, SUM(vlr_sales) AS total_vlr FROM gold.fato_vendas_sku_n WHERE data >= '2024-01-01' AND data <= '2024-12-31';
    """

    # Validação simples para evitar queries destrutivas
    if not query.strip().lower().startswith("select"):
        return "Erro: Apenas consultas de leitura (SELECT) são permitidas."
        
    with pyodbc.connect(CONN_STR) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            print(f"Query executada: {query}")
            return str(results)[:1000] # Limita o tamanho para não estourar o contexto do modelo
        except Exception as e:
            return f"Erro ao executar a query: {str(e)}"
