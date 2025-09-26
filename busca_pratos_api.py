from fastapi import FastAPI
import mysql.connector
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

app = FastAPI()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
    )

@app.get("/")
def root():
    return {"message": "API do Maripili está ativa!"}

@app.get("/entradas-ativas")
def get_entradas_ativas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT Nome, `classificação gastrono` AS categoria, Preço_venda
            FROM Produtos
            WHERE Restaurante = 'Maripili'
              AND `classificação gastrono` = 'Entradas Tapas'
              AND `ativo/suspenso` = 'ativo'
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return resultados

    except Exception as e:
        return {"erro": str(e)}
