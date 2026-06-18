import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Olah, Streamlit")
st.write("Este eh o meu primeiro aplicativo com Streamlit.")
st.header("Este eh um titulo principal maior")
st.subheader("Este eh um subtitulo menor")
st.text("Este eh um texto simples")

data = {
    'Nome' : ['Ana', 'Bruno', 'Carlos'],
    'Idade' : [23, 35, 45],
    'Salario' : [5000, 7000, 9000]
}

df = pd.DataFrame(data)

st.dataframe(df)
st.table(df)

## grafico
fig, ax = plt.subplots()
ax.bar(df['Nome'], df['Salario'])
st.pyplot(fig)

# # ## botao
if st.button('Clique Aqui'):
    st.write('Botao clicado uma vez!')

# # ## slider
idade = st.slider('Selecione sua idade', 0, 100, 25)
st.write(f'Idade selecionada: {idade}')

# # ## Select box
opcao = st.selectbox(
    'Escolha um departamento:',
    ['Recursos Humanos', 'TI', 'Vendas']
)

st.write(f'Departamento selecionado : {opcao}')

## lendo dados externos (poderia ser de banco de dados)
df = pd.read_csv('funcionarios.csv')
#                  
st.dataframe(df)
idade_min = st.slider('Idade minima',0,100,21)
df_filtrado = df[df['Idade'] > idade_min]
st.dataframe(df_filtrado)
#
# ## Criacao de Colunas
col1, col2 = st.columns(2)
with col1:
      st.header('Coluna 1')
      st.write('Conteudo da Coluna 1')
#
with col2:
      st.header('Coluna 2')
      st.write('Conteudo da Coluna 2')
#
#
# ## Sidebar
st.sidebar.header('Filtros')
idade_min = st.sidebar.slider('Idade min', 0, 100, 30)