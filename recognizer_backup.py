import os
import time
import asyncio
import subprocess
from datetime import datetime

from shazamio import Shazam
from database import salvar_musica

URL_RADIO = "http://stm3.srvif.com:8304/;stream.mp3"

PASTA_TEMP = "audio_temp"
os.makedirs(PASTA_TEMP, exist_ok=True)

ultima_musica = ""

def log(msg):
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"[{agora}] {msg}")

def capturar_audio():

    arquivo = f"{PASTA_TEMP}/radio_temp.wav"

    if os.path.exists(arquivo):
        os.remove(arquivo)

    comando = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "quiet",
        "-i",
        URL_RADIO,
        "-t",
        "35",
        "-ac",
        "1",
        "-ar",
        "44100",
        arquivo
    ]

    subprocess.run(comando)

    return arquivo

async def reconhecer_shazam(arquivo):

    shazam = Shazam()

    resultado = await shazam.recognize(arquivo)

    return resultado

log("📻 Monitor Rádio 107 (SHAZAM) iniciado")

while True:

    try:

        log("🎧 Capturando áudio...")

        arquivo = capturar_audio()

        if not os.path.exists(arquivo):
            log("❌ Arquivo não criado")
            time.sleep(10)
            continue

        resultado = asyncio.run(
            reconhecer_shazam(arquivo)
        )

        if "track" in resultado:

            musica = resultado["track"]["title"]
            artista = resultado["track"]["subtitle"]

            atual = f"{musica} - {artista}"

            if atual != ultima_musica:

                salvar_musica(
                    musica,
                    artista
                )

                ultima_musica = atual

                log(f"✅ {musica} - {artista}")

            else:

                log("🔁 Música repetida")

        else:

            log("⚠️ Não identificada")

        if os.path.exists(arquivo):
            os.remove(arquivo)

        time.sleep(15)

    except Exception as erro:

        log(f"❌ Erro: {erro}")

        time.sleep(15)
