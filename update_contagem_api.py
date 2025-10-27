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
        UPDATE contagem SET
            restaurante = %s,
            ingrediente = %s,
            unidade = %s,
            soma = %s,
            contagem_1 = %s,
            contagem_2 = %s,
            contagem_3 = %s,
            data_1 = STR_TO_DATE(%s, '%%d/%%m/%%Y'),
            data_2 = STR_TO_DATE(%s, '%%d/%%m/%%Y'),
            data_3 = STR_TO_DATE(%s, '%%d/%%m/%%Y'),
            quem_contou_1 = %s,
            quem_contou_2 = %s,
            quem_contou_3 = %s
        WHERE id = %s
        """

        params = (
            data.get("restaurante"),
            data.get("ingrediente"),
            data.get("unidade"),
            data.get("soma"),
            data.get("contagem_1"),
            data.get("contagem_2"),
            data.get("contagem_3"),
            data.get("data_1"),
            data.get("data_2"),
            data.get("data_3"),
            data.get("quem_contou_1"),
            data.get("quem_contou_2"),
            data.get("quem_contou_3"),
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
