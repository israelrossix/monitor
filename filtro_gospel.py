import unicodedata

PALAVRAS_BLOQUEADAS = [

    "vinheta",
    "jingle",
    "comercial",
    "propaganda",
    "advertisement",
    "advert",

    "audiox",

    "unknown artist",
    "unknown",

    "relaxing music",
    "sleep music",
    "meditation music",

    "white noise",
    "nature sounds",

    "anime",
    "j-pop",
    "k-pop",
    "cantopop",
    "mandopop",

    "spot",
    "promo",
    "promocao",
    "promoção",
    "merchan",
    "merchandising",
    "intervalo",
    "institucional",
    "chamada",
    "oferecimento",
    "apoio cultural"
]



ARTISTAS_BLOQUEADOS = [

    "ze ramalho",
    "belchior",
    "djavan",
    "shakira",
    "alan walker",
    "avicii",
    "chris martin",
    "van halen",
    "deep purple",
    "thelonious monk",
    "paul mauriat",
    "maynard ferguson",
    "najee",
    "jennifer paige",
    "ennio morricone",
    "vangelis",
    "hans zimmer",
    "james horner",
    "danny elfman",
    "john barry",
    "miklos rozsa",
    "darude",
    "dj sakin",
    "don ross",
    "andy mckee",
    "joe mcbride",
    "sammi cheng",
    "ly hai",
    "twelve titans music",
    "audiomachine",
    "infraction",
    "infraction music",
    "starshine orchestra",
    "london symphony orchestra",
    "london philharmonic orchestra",
    "london festival orchestra",
    "national philharmonic orchestra",
    "mgm studio orchestra",
    "vienna orchestra",
    "pearl harbor soundtrack",
    "nocopyrightvault",
    "nash music library",
    "audiox",
    "efeitos br",
    "bich phuong",
    "lu alone",
    "ive",
    "anderson & vei da pisadinha",
    "marcos e matteus",
    "francisco y sus teclados"
]


def normalizar(texto):

    texto = str(texto)

    texto = unicodedata.normalize(
        "NFKD",
        texto
    )

    texto = "".join(
        c for c in texto
        if not unicodedata.combining(c)
    )

    return texto.lower()

def contem_caracteres_asiaticos(texto):

    for c in texto:

        codigo = ord(c)

        if (
            0x4E00 <= codigo <= 0x9FFF or
            0x3040 <= codigo <= 0x309F or
            0x30A0 <= codigo <= 0x30FF or
            0xAC00 <= codigo <= 0xD7AF
        ):
        
    for artista_bloqueado in ARTISTAS_BLOQUEADOS:

        if artista_bloqueado in texto:
            return False

    return True


    return False

def audio_valido(musica, artista):

    texto = normalizar(
        f"{musica} {artista}"
    )

    if contem_caracteres_asiaticos(texto):
        return False

    if len(str(musica).strip()) < 3:
        return False

    if len(str(artista).strip()) < 2:
        return False

    for palavra in PALAVRAS_BLOQUEADAS:

        if normalizar(palavra) in texto:
            return False


    for artista_bloqueado in ARTISTAS_BLOQUEADOS:

        if artista_bloqueado in texto:
            return False

    return True

