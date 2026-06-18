import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    """Configurações de conexão com Microsoft SQL Server"""
    
    SQL_SERVER = os.getenv('SQL_SERVER')
    SQL_DATABASE = os.getenv('SQL_DATABASE')
    SQL_USERNAME = os.getenv('SQL_USERNAME')
    SQL_PASSWORD = os.getenv('SQL_PASSWORD')
    SQL_DRIVER = os.getenv('SQL_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    @classmethod
    def get_connection_string(cls):
        """Retorna a string de conexão formatada"""
        return (
            f"DRIVER={{{cls.SQL_DRIVER}}};"
            f"SERVER={cls.SQL_SERVER};"
            f"DATABASE={cls.SQL_DATABASE};"
            f"UID={cls.SQL_USERNAME};"
            f"PWD={cls.SQL_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )
    
    @classmethod
    def validate(cls):
        """Valida se todas as configurações necessárias estão presentes"""
        required = ['SQL_SERVER', 'SQL_DATABASE', 'SQL_USERNAME', 'SQL_PASSWORD']
        missing = [attr for attr in required if not getattr(cls, attr)]
        if missing:
            raise ValueError(f"Configurações faltando no .env: {', '.join(missing)}")
        return True
