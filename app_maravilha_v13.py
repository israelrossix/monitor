import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="Monitor Rádio 107",
    page_icon="📻",
    layout="wide"
)

# ==========================================
# TEMA VISUAL V13
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg,#090909,#121212);
}

h1,h2,h3,h4,h5,h6 {
    color: white !important;
}

.card {
    background: #161b22;
    border-left: 3px solid #ff7a00;
    border-radius: 22px;
    padding: 20px;
    margin-bottom: 10px;
    box-shadow: 0 0 4px rgba(255,122,0,.15);
}

.card-title{
    color:#bdbdbd;
    font-size:14px;
}

.card-value{
    color:white;
    font-size:30px;
    font-weight:700;
}

.card-small{
    background:#161b22;
    border-radius:15px;
    padding:15px;
    text-align:center;
}

.card-small h3{
    margin:0;
    color:#ff7a00;
}

.card-small p{
    font-size:26px;
    font-weight:bold;
    color:white;
}

footer {
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# BANCO
# ==========================================

conn = sqlite3.connect(
    "database/radio107.db"
)

df = pd.read_sql_query(
    "SELECT * FROM musicas",
    conn
)

conn.close()

st.write("TOTAL REGISTROS BANCO:", len(df))
st.write("ULTIMO REGISTRO:", df.iloc[-1]["artista"], "-", df.iloc[-1]["musica"])
st.write("ULTIMO TIMESTAMP:", df.iloc[-1]["timestamp"])

if len(df) == 0:

    st.warning(
        "Nenhuma música encontrada."
    )

    st.stop()

# ==========================================
# FILTRO GOSPEL
# ==========================================

ARTISTAS_EXCLUIR = [
    "Kenny G",
    "Hans Zimmer",
    "Vangelis",
    "Party Tyme Karaoke",
    "Network Music Ensemble",
    "Brand X Music",
    "CMORE SMD",
    "Sonido Relajante",
    "Lukas Got Lucky",
    "Universfield",
    "IamDayLight",
    "John Epping",
    "Peaceful Pines",
    "MLY DreaM mUsic",
    "raíSys Music",
    "B Donnelly",
    "B Cantos",
    "Dj RoChA TrEmE TuDo",
    "Smokey Robinson",
    "Pedro Bromfman",
    "Dreamcatcher's Relaxing Band",
    "Noxway",
    "OtoYura.BGM.Lab.",
    "HitsLab",
    "Corporate Express",
    "Ciaran Delany",
    "Rossano Galante",
    "Hollywood Trailer Music Orchestra",
    "Nick Phoenix",
    "William Rydh",
    "BalloonPlanet",
    "Ikson",
    "Marcus Viana",
    "John Williams",
    "Gabriel Yared",
    "Basil Poledouris",
    "Living Colour",
    "Elis Regina",
    "Titãs",
    "Raul Seixas",
    "Os Mutantes",
    "Pedro Mariano",
    "小奶瓶",
    "小童話大世界"
]

df = df[
    ~df["artista"].isin(
        ARTISTAS_EXCLUIR
    )
]

# ==========================================
# DATAS
# ==========================================

df["timestamp"] = pd.to_datetime(
    df["timestamp"]
)

df["mes"] = (
    df["timestamp"]
    .dt.strftime("%Y-%m")
)

meses = sorted(
    df["mes"].unique(),
    reverse=True
)

# ==========================================
# CABEÇALHO
# ==========================================

col_logo,col_titulo,col_filtro = st.columns(
    [1,4,2]
)

with col_logo:

    st.image(
        "assets/logo89.png",
        width=340
    )

with col_titulo:

    st.markdown("""
<h1>📻 MONITOR RÁDIO 107</h1>

<h2 style="color:#ff7a00;">
Rádio 89.1 Maravilha
</h2>

<p><i>
A Rádio de todas as igrejas que toca o som do céu!
</i></p>
""", unsafe_allow_html=True)

with col_filtro:

    mes_selecionado = st.selectbox(
        "Período",
        meses
    )

df = df[
    df["mes"] ==
    mes_selecionado
]
# ==========================================
# INDICADORES
# ==========================================

hoje = pd.Timestamp.now().date()

df_hoje = df[
    df["timestamp"].dt.date == hoje
]

artistas_unicos = (
    df["artista"]
    .nunique()
)

ultima_gravacao = (
    df["timestamp"]
    .max()
)

status_monitor = "ONLINE"

ultima_atualizacao = (
    ultima_gravacao
    .strftime("%d/%m/%Y %H:%M:%S")
)

# ==========================================
# CARDS EXECUTIVOS
# ==========================================

st.markdown("<br>", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)

with c1:

    st.markdown(f"""
<div class="card">
<div class="card-title">
🎵 MÚSICAS HOJE
</div>
<div class="card-value">
{len(df_hoje)}
</div>
</div>
""", unsafe_allow_html=True)

with c2:

    st.markdown(f"""
<div class="card">
<div class="card-title">
📅 MÚSICAS NO PERÍODO
</div>
<div class="card-value">
{len(df)}
</div>
</div>
""", unsafe_allow_html=True)

with c3:

    st.markdown(f"""
<div class="card">
<div class="card-title">
🎤 ARTISTAS ÚNICOS
</div>
<div class="card-value">
{artistas_unicos}
</div>
</div>
""", unsafe_allow_html=True)

with c4:

    st.markdown(f"""
<div class="card">
<div class="card-title">
📻 STATUS DO MONITOR
</div>

<div class="card-value">
{status_monitor}
</div>

<div style="font-size:12px;color:#bdbdbd;">
Última atualização:<br>
{ultima_atualizacao}
</div>

</div>
""", unsafe_allow_html=True)

# ==========================================
# PRODUÇÃO POR HORA
# ==========================================

st.markdown("## 📊 Produção Musical por Hora")

hora_df = df_hoje.copy()

if len(hora_df) > 0:

    hora_df["hora"] = (
        hora_df["timestamp"]
        .dt.strftime("%H:00")
    )

    exec_hora = (
        hora_df.groupby("hora")
        .size()
        .reset_index(
            name="execucoes"
        )
    )

    fig_hora = px.line(
        exec_hora,
        x="hora",
        y="execucoes",
        markers=True
    )

    fig_hora.update_traces(
        line_color="#ff7a00",
        marker_color="#ff7a00"
    )

    fig_hora.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig_hora,
        width="stretch"
    )

# ==========================================
# FAIXAS HORÁRIAS
# ==========================================

st.markdown(
    "## 🕒 Produção por Faixa Horária"
)

periodos = (
    df.groupby("periodo")
    .size()
    .reset_index(
        name="execucoes"
    )
)

f1,f2,f3,f4 = st.columns(4)

def valor_periodo(nome):

    filtro = periodos[
        periodos["periodo"] == nome
    ]

    if len(filtro) == 0:
        return 0

    valor = int(
        filtro["execucoes"]
        .iloc[0]
    )

    total = int(
        periodos["execucoes"].sum()
    )

    percentual = round(
        (valor / total) * 100,
        1
    )

    return f"{valor}<br><span style='font-size:14px;color:#bdbdbd'>{percentual}%</span>"

f1.markdown(
f"""
<div class="card-small">
<h3>🌙 Madrugada</h3>
<p>{valor_periodo("Madrugada")}</p>
</div>
""",
unsafe_allow_html=True
)

f2.markdown(
f"""
<div class="card-small">
<h3>🌅 Manhã</h3>
<p>{valor_periodo("Manhã")}</p>
</div>
""",
unsafe_allow_html=True
)

f3.markdown(
f"""
<div class="card-small">
<h3>☀️ Tarde</h3>
<p>{valor_periodo("Tarde")}</p>
</div>
""",
unsafe_allow_html=True
)

f4.markdown(
f"""
<div class="card-small">
<h3>🌙 Noite</h3>
<p>{valor_periodo("Noite")}</p>
</div>
""",
unsafe_allow_html=True
)
# ==========================================
# DESTAQUES DA PROGRAMAÇÃO
# ==========================================

st.markdown("## 🏆 Destaques da Programação")

ranking_musicas = (
    df.groupby(["musica","artista"])
    .size()
    .reset_index(name="execucoes")
    .sort_values(
        "execucoes",
        ascending=False
    )
)

ranking_artistas = (
    df.groupby("artista")
    .agg(
        execucoes=("artista","size"),
        musicas_unicas=("musica","nunique")
    )
    .reset_index()
    .sort_values(
        "execucoes",
        ascending=False
    )
)

musica_lider = "-"
artista_lider = "-"

if len(ranking_musicas) > 0:
    musica_lider = ranking_musicas.iloc[0]["musica"]

if len(ranking_artistas) > 0:
    artista_lider = ranking_artistas.iloc[0]["artista"]

d1,d2 = st.columns(2)

with d1:

    st.markdown(f"""
<div class="card">
<div class="card-title">
🎵 MÚSICA LÍDER DO PERÍODO
</div>
<div class="card-value" style="font-size:22px;">
{musica_lider}
</div>
</div>
""", unsafe_allow_html=True)

with d2:

    st.markdown(f"""
<div class="card">
<div class="card-title">
🎤 ARTISTA LÍDER DO PERÍODO
</div>
<div class="card-value" style="font-size:22px;">
{artista_lider}
</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# RANKING DE ARTISTAS
# ==========================================

st.markdown("## 🎤 Ranking de Artistas")

top_artistas = ranking_artistas.head(15)

st.dataframe(
    top_artistas[
        ["artista","execucoes","musicas_unicas"]
    ],
    width="stretch",
    height=420
)

fig_artistas = px.bar(
    top_artistas,
    x="execucoes",
    y="artista",
    orientation="h"
)

fig_artistas.update_traces(
    marker_color="#ff7a00"
)

fig_artistas.update_layout(
    template="plotly_dark",
    height=550,
    yaxis={"categoryorder":"total ascending"}
)

st.plotly_chart(
    fig_artistas,
    width="stretch"
)

# ==========================================
# MÚSICAS DO ARTISTA
# ==========================================

st.markdown(
    "## 🎼 Músicas Mais Tocadas do Artista"
)

lista_artistas = sorted(
    df["artista"]
    .dropna()
    .unique()
)

indice_padrao = 0

if artista_lider in lista_artistas:
    indice_padrao = lista_artistas.index(
        artista_lider
    )

artista_escolhido = st.selectbox(
    "Selecione um artista",
    lista_artistas,
    index=indice_padrao
)

df_artista = df[
    df["artista"] ==
    artista_escolhido
]

musicas_artista = (
    df_artista.groupby("musica")
    .size()
    .reset_index(
        name="execucoes"
    )
    .sort_values(
        "execucoes",
        ascending=False
    )
)

fig_musicas_artista = px.bar(
    musicas_artista.head(15),
    x="execucoes",
    y="musica",
    orientation="h"
)

fig_musicas_artista.update_traces(
    marker_color="#ff7a00"
)

fig_musicas_artista.update_layout(
    template="plotly_dark",
    height=500,
    yaxis={
        "categoryorder":"total ascending"
    }
)

st.plotly_chart(
    fig_musicas_artista,
    width="stretch"
)
# ==========================================
# PRINCIPAIS MÚSICAS POR FAIXA HORÁRIA
# ==========================================

st.markdown(
    "## 🎵 Principais Músicas por Faixa Horária"
)

aba1,aba2,aba3,aba4 = st.tabs(
    [
        "🌙 Madrugada",
        "🌅 Manhã",
        "☀️ Tarde",
        "🌙 Noite"
    ]
)

def top_periodo(nome):

    return (
        df[
            df["periodo"] == nome
        ]
        .groupby(
            ["musica","artista"]
        )
        .size()
        .reset_index(
            name="execucoes"
        )
        .sort_values(
            "execucoes",
            ascending=False
        )
        .head(15)
    )

with aba1:

    st.dataframe(
        top_periodo("Madrugada"),
        width="stretch",
        height=400
    )

with aba2:

    st.dataframe(
        top_periodo("Manhã"),
        width="stretch",
        height=400
    )

with aba3:

    st.dataframe(
        top_periodo("Tarde"),
        width="stretch",
        height=400
    )

with aba4:

    st.dataframe(
        top_periodo("Noite"),
        width="stretch",
        height=400
    )

# ==========================================
# PRODUÇÃO POR DIA
# ==========================================

st.markdown(
    "## 📅 Produção Musical por Dia"
)

dia_df = df.copy()

dia_df["dia"] = (
    dia_df["timestamp"]
    .dt.strftime("%d/%m")
)

exec_dia = (
    dia_df.groupby("dia")
    .size()
    .reset_index(
        name="execucoes"
    )
)

fig_dia = px.bar(
    exec_dia,
    x="dia",
    y="execucoes"
)

fig_dia.update_traces(
    marker_color="#ff7a00"
)

fig_dia.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    fig_dia,
    width="stretch"
)

# ==========================================
# RESUMO POR FAIXA HORÁRIA
# ==========================================

st.markdown(
    "## 📈 Distribuição da Programação"
)

fig_periodos = px.bar(
    periodos,
    x="periodo",
    y="execucoes",
    text_auto=True
)

fig_periodos.update_traces(
    marker_color="#ff7a00"
)

fig_periodos.update_layout(
    template="plotly_dark",
    height=450
)

st.plotly_chart(
    fig_periodos,
    width="stretch"
)

# ==========================================
# RODAPÉ
# ==========================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center'>

<h3 style='color:#ff7a00'>
Rádio 89.1 Maravilha
</h3>

<p style='color:white'>
A Rádio de todas as igrejas que toca o som do céu!
</p>

<p style='color:#9ca3af'>
Monitor Rádio 107
</p>

<p style='color:#9ca3af'>
Desenvolvido por Israel Rossi Alves
</p>

</div>
""",
unsafe_allow_html=True
)
