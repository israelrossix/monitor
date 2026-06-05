import os
import time
import json
import asyncio
import subprocess
from datetime import datetime

from shazamio import Shazam
from acrcloud.recognizer import ACRCloudRecognizer

from database import salvar_musica

from acrcloud_config import (
    ACR_HOST,
    ACR_ACCESS_KEY,
    ACR_ACCESS_SECRET
)

URL_RADIO = "http://stm3.srvif.com:8304/;stream.mp3"

PASTA_TEMP = "audio_temp"
os.makedirs(PASTA_TEMP, exist_ok=True)

ultima_musica = ""

acr = ACRCloudRecognizer({
    "host": ACR_HOST,
    "access_key": ACR_ACCESS_KEY,
    "access_secret": ACR_ACCESS_SECRET,
    "timeout": 10
})


def log(msg):
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"[{agora}] {msg}")


def capturar_audio():

    arquivo = f"{PASTA_TEMP}/radio_temp.wav"

    if os.path.exists(arquivo):
        os.remove(arquivo)

    subprocess.run([
        "ffmpeg",
        "-y",
        "-loglevel",
        "quiet",
        "-i",
        URL_RADIO,
        "-t",
        "25",
        "-ac",
        "1",
        "-ar",
        "44100",
        arquivo
    ])

    return arquivo


async def reconhecer_shazam(arquivo):

    try:

        shazam = Shazam()

        resultado = await shazam.recognize(
            arquivo
        )

        if "track" not in resultado:
            return None

        musica = resultado["track"]["title"]
        artista = resultado["track"]["subtitle"]

        return musica, artista

    except Exception:
        return None


def reconhecer_acrcloud(arquivo):

    try:

        with open(arquivo, "rb") as f:
            buffer = f.read()

        resultado = acr.recognize_by_filebuffer(
            buffer,
            0
        )

        dados = json.loads(resultado)

        if dados["status"]["code"] != 0:
            return None

        musica = dados["metadata"]["music"][0]["title"]
        artista = dados["metadata"]["music"][0]["artists"][0]["name"]

        return musica, artista

    except Exception:
        return None


log("📻 Monitor Rádio 107 HÍBRIDO")
log("🎯 Shazam + ACRCloud")

while True:

    inicio = time.time()

    try:

        log("🎧 Capturando áudio...")

        arquivo = capturar_audio()

        identificado = None
        origem = ""

        log("🔍 Consultando Shazam...")

        identificado = asyncio.run(
            reconhecer_shazam(arquivo)
        )

        if identificado:

            origem = "SHAZAM"

        else:

            log("🔍 Consultando ACRCloud...")

            identificado = reconhecer_acrcloud(
                arquivo
            )

            origem = "ACRCLOUD"

        if identificado:

            musica, artista = identificado

            atual = f"{musica} - {artista}"

            if atual != ultima_musica:

                salvar_musica(
                    musica,
                    artista
                )

                ultima_musica = atual

                log(
                    f"✅ {origem} | {musica} - {artista}"
                )

            else:

                log("🔁 Música repetida")

        else:

            log("⚠️ Não identificada")

        if os.path.exists(arquivo):
            os.remove(arquivo)

        tempo_gasto = time.time() - inicio

        espera = max(
            0,
            60 - tempo_gasto
        )

        log(
            f"⏳ Próxima consulta em {int(espera)}s"
        )

        time.sleep(espera)

    except Exception as erro:

        log(
            f"❌ Erro: {erro}"
        )

        time.sleep(60)
