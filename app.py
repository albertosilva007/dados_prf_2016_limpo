import streamlit as st
import pandas as pd
import plotly.express as px

# Título
st.title("📊 Acidentes Rodoviários no Brasil - PRF 2016")
st.markdown("Uma análise dos acidentes rodoviários registrados pela PRF em 2016 com foco em identificar padrões críticos e sugerir ações preventivas.")

# Carregamento e tratamento dos dados


@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_prf_2016_limpo.csv",
                     sep=",")  # Ajuste do separador
    df.columns = df.columns.str.strip().str.lower()  # Padronização
    return df


df = carregar_dados()

# Visualização das colunas disponíveis de forma amigável
st.markdown("### 📋 Colunas disponíveis no DataFrame:")
for col in df.columns:
    st.markdown(f"- `{col}`")

# Filtros laterais
ufs = st.sidebar.multiselect(
    "Selecionar estados (UF)",
    options=df["uf"].unique(),
    default=df["uf"].unique()
)
df_filtrado = df[df["uf"].isin(ufs)]

# Conversão de datas
df_filtrado['data_inversa'] = pd.to_datetime(
    df_filtrado['data_inversa'], format='%d/%m/%Y', errors='coerce'
)
df_filtrado['mes'] = df_filtrado['data_inversa'].dt.month

# Gráfico 1: Acidentes por mês
acidentes_por_mes = df_filtrado.groupby("mes").size()
fig_mes = px.line(
    x=acidentes_por_mes.index,
    y=acidentes_por_mes.values,
    labels={"x": "Mês", "y": "Quantidade de Acidentes"},
    title="📅 Acidentes por Mês"
)
st.plotly_chart(fig_mes)

# Gráfico 2: Acidentes por condição climática
cond_clima = df_filtrado["condicao_metereologica"].value_counts().reset_index()
cond_clima.columns = ['Condição', 'Total']
fig_clima = px.bar(
    cond_clima, x="Condição", y="Total",
    title="🌦️ Acidentes por Condição Climática"
)
st.plotly_chart(fig_clima)

# Gráfico 3: Acidentes por fase do dia
fase_dia = df_filtrado["fase_dia"].value_counts().reset_index()
fase_dia.columns = ['Fase do Dia', 'Total']
fig_fase = px.pie(
    fase_dia, names="Fase do Dia", values="Total",
    title="🌙 Acidentes por Fase do Dia"
)
st.plotly_chart(fig_fase)

# Gráfico 4: Acidentes por hora do dia
df_filtrado['hora'] = pd.to_datetime(
    df_filtrado['horario'], format="%H:%M:%S", errors='coerce'
).dt.hour
acidentes_por_hora = df_filtrado['hora'].value_counts(
).sort_index().reset_index()
acidentes_por_hora.columns = ['Hora', 'Total']
fig_hora = px.bar(
    acidentes_por_hora, x="Hora", y="Total",
    title="⏰ Acidentes por Hora do Dia"
)
st.plotly_chart(fig_hora)

# Gráfico 5: Municípios com mais acidentes fatais
fatais = df_filtrado[df_filtrado["classificacao_acidente"] == 2]
top_municipios = fatais["municipio"].value_counts().head(10).reset_index()
top_municipios.columns = ['Município', 'Total Fatais']
fig_mun = px.bar(
    top_municipios, x="Município", y="Total Fatais",
    title="🏡 Municípios com Mais Acidentes Fatais"
)
st.plotly_chart(fig_mun)

# Conclusões
st.header("🧠 Conclusões e Insights")
st.markdown("""
- 🚨 Os meses de férias (janeiro, julho, dezembro) concentram mais acidentes.
- 🌧️ Acidentes ocorrem majoritariamente sob tempo claro, o que sugere falhas humanas.
- 🌙 A madrugada e o início da manhã concentram mais acidentes graves.
- 🏙️ Alguns municípios são recorrentes em fatalidades, podendo ser alvos de ações específicas.

### 📌 Recomendações:
- Campanhas educativas noturnas e em horários críticos.
- Melhor sinalização em municípios com alta letalidade.
- Reforço de fiscalização em BRs movimentadas.

**Fonte**: Polícia Rodoviária Federal - Dados Públicos de 2016.
""")
