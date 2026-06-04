import sqlite3
from datetime import datetime, timedelta

from supabase_db import supabase

DB_PATH = "database/radio107.db"


def conectar():
    return sqlite3.connect(DB_PATH)


def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS musicas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        musica TEXT,
        artista TEXT,
        data TEXT,
        horario TEXT,
        periodo TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


def definir_periodo(hora):

    hora = int(hora)

    if 0 <= hora < 6:
        return "Madrugada"

    elif 6 <= hora < 12:
        return "Manhã"

    elif 12 <= hora < 18:
        return "Tarde"

    return "Noite"


def musica_ja_existe(musica, artista):

    conn = conectar()
    cursor = conn.cursor()

    limite = datetime.now() - timedelta(minutes=30)

    cursor.execute("""
    SELECT *
    FROM musicas
    WHERE musica = ?
    AND artista = ?
    AND timestamp >= ?
    """, (
        musica,
        artista,
        limite.strftime("%Y-%m-%d %H:%M:%S")
    ))

    resultado = cursor.fetchone()

    conn.close()

    return resultado is not None


def salvar_musica(musica, artista):

    if musica_ja_existe(musica, artista):
        print("Música repetida ignorada.")
        return

    agora = datetime.now()

    data = agora.strftime("%Y-%m-%d")
    horario = agora.strftime("%H:%M:%S")
    periodo = definir_periodo(agora.strftime("%H"))
    timestamp = agora.strftime("%Y-%m-%d %H:%M:%S")

    # SQLite
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO musicas (
        musica,
        artista,
        data,
        horario,
        periodo,
        timestamp
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        musica,
        artista,
        data,
        horario,
        periodo,
        timestamp
    ))

    conn.commit()
    conn.close()

    # Supabase
    try:

        supabase.table(
            "musicas"
        ).insert({
            "musica": musica,
            "artista": artista,
            "data": data,
            "horario": horario,
            "periodo": periodo,
            "timestamp": timestamp
        }).execute()

        print("✅ Gravado no Supabase")

    except Exception as erro:

        print(
            f"Erro Supabase: {erro}"
        )


def criar_tabela_se_nao_existir():
    criar_tabela()


if __name__ == "__main__":
    criar_tabela()
