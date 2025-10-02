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
    host = os.getenv("DB_HOST")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    database = os.getenv("DB_NAME")

    # log seguro para depuração
    print(f"🔎 Conectando ao banco: host={host}, port={port}, user={user}, db={database}")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )

# ---------- Endpoint para testar a conexão ----------
@app.get("/entradas-ativas")
def get_entradas_ativas():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "Conexão OK ✅"}
    except Exception as e:
        return {"erro": str(e)}
