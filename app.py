import streamlit as st
import pandas as pd
import numpy as np

st.image("logo_atualizada.png", caption="Leônidas Business Intelligence")

st.title('Números de corridas da UBER em Nova York 2024')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Criando um elemento de texto avisando ao usuário que os dados estão carregando.
data_load_state = st.text('Aguarde, carregando dados...')
# Carregando até 10,000 linhas de dados no dataframe.
data = load_data(10000)
# Informando ao usuário que os dados foram carregados com sucesso.
data_load_state.text('Ok, dados atualizados!')

if st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados brutos')
    st.write(data)

st.subheader('Números de corridas por hora')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Um número no intervalor de 0-23.
hour_to_filter = st.slider('FILTRO:  ->  .::CORRIDAS POR HORÁRIOS::.', 0, 23, 17) # minimo: 0h, maximo: 23h, horas padrão: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Mapa das corridas em %s:00' % hour_to_filter)
st.map(filtered_data)


st.subheader('__________________________________________________\n - Dados fornecido pela Amazom AWS\n . by Leônidas Business Intelligence\n ..::insights & decisões::..')