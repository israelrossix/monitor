import os
import time
import json
import subprocess
from datetime import datetime

from acrcloud.recognizer import ACRCloudRecognizer

from database import salvar_musica
from config import ACR_CONFIG

recognizer = ACRCloudRecognizer(ACR_CONFIG)

URL_RADIO = "http://stm3.srvif.com:8304/;stream.mp3"

PASTA_TEMP = "audio_temp"

os.makedirs(PASTA_TEMP, exist_ok=True)

ultima_musica = ""

def log(mensagem):

    agora = datetime.now().strftime("%H:%M:%S")

    print(f"[{agora}] {mensagem}")

def capturar_audio():

    arquivo = f"{PASTA_TEMP}/radio_temp.mp3"

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
        "20",
        "-acodec",
        "mp3",
        arquivo
    ]

    resultado = subprocess.run(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    return arquivo

def reconhecer_musica(arquivo):

    with open(arquivo, "rb") as audio_file:

        buffer = audio_file.read()

    resultado = recognizer.recognize_by_filebuffer(buffer, 0)

    return json.loads(resultado)

log("📻 Monitor Rádio 107 iniciado")

while True:

    try:

        log("🎧 Capturando áudio...")

        arquivo_audio = capturar_audio()

        if not os.path.exists(arquivo_audio):

            log("❌ Arquivo não foi criado")

            time.sleep(5)

            continue

        tamanho = os.path.getsize(arquivo_audio)

        if tamanho < 10000:

            log("⚠️ Áudio muito pequeno")

            time.sleep(5)

            continue

        resultado = reconhecer_musica(arquivo_audio)

        status = resultado.get("status", {}).get("msg")

        if status == "Success":

            musica = resultado["metadata"]["music"][0]["title"]

            artista = resultado["metadata"]["music"][0]["artists"][0]["name"]

            musica_atual = f"{musica} - {artista}"

            if musica_atual != ultima_musica:

                salvar_musica(musica, artista)

                ultima_musica = musica_atual

                log(f"✅ Tocando: {musica} - {artista}")

            else:

                log("🔁 Música repetida")

        else:

            log("⚠️ Música não identificada")

        if os.path.exists(arquivo_audio):

            os.remove(arquivo_audio)

        time.sleep(5)

    except Exception as erro:

        log(f"❌ Erro: {erro}")

        time.sleep(10)
