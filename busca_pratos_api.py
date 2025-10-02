from fastapi import FastAPI
import mysql.connector
import os

app = FastAPI(title="API Restaurante Maripili")

# ---------- Endpoints básicos ----------
@app.get("/")
def read_root():
    return {"status": "API do Maripili funcionando ✅"}

@app.get("/health")
def health_check():
    return {"health": "ok", "message": "API está no ar e respondendo 🚀"}

# ---------- Conexão com MySQL ----------
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
    )

# ---------- Endpoint com dados do banco ----------
@app.get("/entradas-ativas")
def get_entradas_ativas():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT Nome, Restaurante, p_class_gastrono, p_preco_venda
        FROM tabela_pratos
        WHERE p_class_gastrono = 'Entradas Tapas'
          AND p_ativo = 'ativo'
        """
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()
        return {"entradas_ativas": results}

    except Exception as e:
        return {"erro": str(e)}
