import asyncpg
import os
from datetime import datetime
import locale
from dotenv import load_dotenv, find_dotenv
from werkzeug.exceptions import abort


load_dotenv(find_dotenv())
PG_HOST = "localhost"
PG_DB_NAME = os.environ.get('PG_DB_NAME')
PG_DB_USER = os.environ.get('PG_DB_USER')
PG_DB_PASS = os.environ.get('PG_DB_PASS')


async def get_from_pg():
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    today = datetime.now()
    mm = f"0{today.month}" if today.month < 10 else str(today.month)
    dd = f"0{today.day}" if today.day < 10 else str(today.day)
    sql_req = f"""
                    SELECT
                        pname,
                        bdate,
                        profession,
                        photourl,
                        weburl
                    FROM people
                    WHERE bdate::text LIKE ('____-{mm}-{dd}')
                    ORDER BY bdate DESC;
                    """

    try:
        connection = await asyncpg.connect(
            host=PG_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=120)
        res = await connection.fetch(sql_req)
        await connection.close()
        if res is None:
            abort(404)
        return res
    except Exception as e:
        print(f'[ERROR] - {e}')
        return []


async def add_question(name, question, email):
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    today = datetime.now()
    sql_req = f"""
        INSERT INTO question 
        (user_name, user_question, user_email, date) 
        VALUES 
        ('{name}', '{question}', '{email}', '{today}');
        """

    try:
        connection = await asyncpg.connect(
            host=PG_HOST,
            database=PG_DB_NAME,
            user=PG_DB_USER,
            password=PG_DB_PASS,
            timeout=120)
        await connection.execute(sql_req)
        return True
    except Exception as e:
        print(f'[ERROR] - {e}')
        return False
