import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("Native JavaScript Injection")

# Use st.html to inject directly into the main app frame
st.html(
    """
     // Initialize the echarts instance based on the prepared dom
      var myChart = echarts.init(document.getElementById('main'));

      // Specify the configuration items and data for the chart
      var option = {
        title: {
          text: 'ECharts Getting Started Example'
        },
        tooltip: {},
        legend: {
          data: ['sales']
        },
        xAxis: {
          data: ['Shirts', 'Cardigans', 'Chiffons', 'Pants', 'Heels', 'Socks']
        },
        yAxis: {},
        series: [
          {
            name: 'sales',
            type: 'bar',
            data: [5, 20, 36, 10, 10, 20]
          }
        ]
      };

      // Display the chart using the configuration and the data defined above.
      myChart.setOption(option);
    """,
)


# data = {
#     'Nome' : ['Ana', 'Bruno', 'Carlos'],
#     'Idade' : [23, 35, 45],
#     'Salario' : [5000, 7000, 9000]
# }

# df = pd.DataFrame(data)

# st.dataframe(df)
# st.table(df)

# ## grafico
# fig, ax = plt.subplots()
# ax.bar(df['Nome'], df['Salario'])
# st.pyplot(fig)

# # # ## botao
# if st.button('Clique Aqui'):
#     st.write('Botao clicado uma vez!')

# # # ## slider
# idade = st.slider('Selecione sua idade', 0, 100, 25)
# st.write(f'Idade selecionada: {idade}')

# # # ## Select box
# opcao = st.selectbox(
#     'Escolha um departamento:',
#     ['Recursos Humanos', 'TI', 'Vendas']
# )

# st.write(f'Departamento selecionado : {opcao}')

# ## lendo dados externos (poderia ser de banco de dados)
# df = pd.read_csv('funcionarios.csv')
# #                  
# st.dataframe(df)
# idade_min = st.slider('Idade minima',0,100,21)
# df_filtrado = df[df['Idade'] > idade_min]
# st.dataframe(df_filtrado)
# #
# # ## Criacao de Colunas
# col1, col2 = st.columns(2)
# with col1:
#       st.header('Coluna 1')
#       st.write('Conteudo da Coluna 1')
# #
# with col2:
#       st.header('Coluna 2')
#       st.write('Conteudo da Coluna 2')
# #
# #
# # ## Sidebar
# st.sidebar.header('Filtros')
# idade_min = st.sidebar.slider('Idade min', 0, 100, 30)


