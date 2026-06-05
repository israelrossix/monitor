import json
import subprocess
from acrcloud.recognizer import ACRCloudRecognizer

from acrcloud_config import (
    ACR_HOST,
    ACR_ACCESS_KEY,
    ACR_ACCESS_SECRET
)

config = {
    "host": ACR_HOST,
    "access_key": ACR_ACCESS_KEY,
    "access_secret": ACR_ACCESS_SECRET,
    "timeout": 10
}

print("Capturando 25 segundos da rádio...")

subprocess.run([
    "ffmpeg",
    "-y",
    "-loglevel",
    "quiet",
    "-i",
    "http://stm3.srvif.com:8304/;stream.mp3",
    "-t",
    "25",
    "teste_acr.wav"
])

recognizer = ACRCloudRecognizer(config)

with open("teste_acr.wav", "rb") as f:
    buffer = f.read()

resultado = recognizer.recognize_by_filebuffer(buffer, 0)

dados = json.loads(resultado)

print(json.dumps(dados, indent=2, ensure_ascii=False))
