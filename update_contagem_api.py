from fastapi import FastAPI, Request
import mysql.connector
import os

app = FastAPI()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/update_contagem")
async def update_contagem(request: Request):
    data = await request.json()
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
        UPDATE contagem
        SET
            contagem_1 = %s,
            data_1 = STR_TO_DATE(%s, '%%Y-%%m-%%d'),
            quem_contou_1 = %s
        WHERE id = %s
        """

        params = (
            data.get("contagem_1"),
            data.get("data_1"),
            data.get("quem_contou_1"),
            data.get("id")
        )

        cursor.execute(sql, params)
        conn.commit()
        return {"success": True, "rows_affected": cursor.rowcount}

    except Exception as e:
        return {"success": False, "error": str(e)}

    finally:
        cursor.close()
        conn.close()
