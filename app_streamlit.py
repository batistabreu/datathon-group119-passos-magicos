import streamlit as st 
import pandas as pd
import plotly.graph_objects as go
from joblib import load
import plotly.express as px
import numpy as np

#Funções de leitura
import pandas as pd

# Função para tratar as colunas de diferentes anos
def tratativa_base_passos_magicos(df, year_list):
    combined_df = pd.DataFrame()

    for year in year_list:
        # Filtra as colunas que terminam com o ano especificado
        cols_with_year = [col for col in df.columns if col.endswith(f'_{year}')]

        # Cria novas colunas sem o ano
        new_columns = ['NOME', 'ANO'] + [col[:-5] for col in cols_with_year]

        # Cria um novo DataFrame temporário
        temp_df = pd.DataFrame(columns=new_columns)

        # Preenche o novo DataFrame com os dados correspondentes
        for index, row in df.iterrows():
            new_row = [row['NOME'], year] + [row[col] for col in cols_with_year]
            temp_df.loc[index] = new_row

        # Adiciona os dados processados ao DataFrame combinado
        combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

    return combined_df

# Função para tratar a coluna FASE_TURMA para o ano de 2020
def tratar_fase_turma(df):
    df.loc[df['ANO'] == '2020', 'FASE'] = df['FASE_TURMA'].str[0]
    df.loc[df['ANO'] == '2020', 'TURMA'] = df['FASE_TURMA'].str[1:]
    return df

# Função para limpar o dataset removendo linhas e colunas indesejadas
def cleaning_dataset(df):
    _df = df.dropna(subset=df.columns.difference(['NOME', 'ANO']), how='all')  # Drop linhas com NaN em todas as colunas exceto 'NOME' e 'ANO'
    _df = _df[~_df.isna().all(axis=1)]  # Remove linhas com apenas NaN
    return _df

# Função para manter apenas as colunas sem valores nulos
def drop_null_columns(df):
    df = df.dropna(axis=1, how='any')  # Drop colunas com qualquer valor nulo
    return df

# Função para restaurar colunas específicas de outro DataFrame
def restore_columns(df, df_source, columns):
    for col in columns:
        df.loc[:, col] = df_source[col]
    return df

# Função para arredondar as colunas para 2 casas decimais
def round_columns(df, columns):
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')
    df[columns] = df[columns].round(2)
    return df

# Função para filtrar valores indesejados em uma coluna específica
def filter_unwanted_values(df, column, unwanted_values):
    df = df[~df[column].isin(unwanted_values)]
    return df

# Pipeline para executar todas as funções
def pipeline_passos_magicos(df, year_list, colunas_para_arredondar, valores_indesejados):
    df_combined = tratativa_base_passos_magicos(df, year_list)
    df_combined = tratar_fase_turma(df_combined)
    df_cleaned = cleaning_dataset(df_combined)
    df_cleaned = drop_null_columns(df_cleaned)
    
    # Restaurar colunas
    df_cleaned = restore_columns(df_cleaned, df_combined, ['PONTO_VIRADA', 'INDICADO_BOLSA'])
    
    # Arredondar colunas numéricas
    df_cleaned = round_columns(df_cleaned, colunas_para_arredondar)
    
    # Filtrar valores indesejados na coluna 'PEDRA'
    df_final = filter_unwanted_values(df_cleaned, 'PEDRA', valores_indesejados)
    
    return df_final

# Configurações Gerais da Página
st.set_page_config(page_title="Tech Challenge - Passos Mágicos & FIAP - Grupo 119", layout="wide")

st.markdown("""
<style>
.custom-card {
    text-align: center;
    margin: 20px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15); /* Sombra para dar um efeito elevado */
    font-size: 20px;
    background-color: #333333; /* Cor de fundo dos cartões */
    color: #FFFFFF; /* Cor do texto */
}
.custom-card .value {
    font-size: 30px;
    font-weight: bold;
}
.custom-card .label {
    font-size: 18px;
    color: #BBBBBB; /* Cor do rótulo */
    margin-top: 5px;
}
.custom-hr {
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0));
}
.small-text {
    font-size: 14px;
    color: #666666;
}
.stNumberInput > div {
    padding: 5px;
    width: 100px;  /* Ajuste o valor conforme necessário */
}
</style>
""", unsafe_allow_html=True)

# Sidebar para navegação
page = st.sidebar.selectbox("Escolha a Página", ["Análises", "Deploy do Modelo"])

# Carregar os dados
df_passos_magicos = pd.read_csv(r'PEDE_PASSOS_DATASET_FIAP.csv', sep=';')
year_list = ['2020', '2021', '2022']
colunas_para_arredondar = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN']
valores_indesejados = ['#NULO!', 'D9891/2A']

# Executar o pipeline completo
df_pm_not_nulls = pipeline_passos_magicos(df_passos_magicos, year_list, colunas_para_arredondar, valores_indesejados)

# Página de Análises
if page == "Análises":
    ## BLOCO 1 - INTRODUÇÃO
    st.write('# I. Introdução')
    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)

    # Texto de contexto
    st.markdown("""
    <p class="small-text">
                
    A Associação Passos Mágicos dedica-se à transformação da vida de crianças e jovens de baixa renda da cidade de Embu-Guaçu, desde o ano de 1992,
    proporcionando melhores oportunidades de vida para aqueles que mais precisam.

    O projeto oferece educação de qualidade, apoio psicológico e psicopedagógico, além da promoção de uma visão ampliada do mundo e do protagonismo juvenil.

    Dentro da instituição, existem indicadores criados com base nos princípios do projeto e que são usados para acompanhar o desenvolvimento do aluno.

    Com base nisso, esse painel visa entregar dois modelos de Machine Learning:
    <ul>
        <li>Previsibilidade do ponto de virada.</li>
        <li>Previsibilidade da indicação para uma bolsa de estudos.</li>
    </ul>
    </p>
    """, unsafe_allow_html=True)

    ## BLOCO 2 - ANÁLISE DOS DADOS
    st.write('# II. Conhecendo os indicadores')

    st.markdown("""
    <p>Para entendimento dos próximos passos, vamos passar rapidamente a definição e como é feita a coleta dos indicadores que compõem a construção da Pedra-Conceito:</p>
    <ul>
        <li><strong>IAN - Indicador de Adequação de Nível:</strong> através de registros administrativos</li>
        <li><strong>IDA - Indicador de Desempenho Acadêmico:</strong> através de provas ao longo do período</li>
        <li><strong>IEG - Indicador de Engajamento:</strong> através de registros de entrega de lições de casa e de voluntariado</li>
        <li><strong>IAA - Indicador de Autoavaliação:</strong> através de um questionário individual</li>
        <li><strong>IPS - Indicador Psicossocial:</strong> através de um questionário individual</li>
        <li><strong>IPP - Indicador Psicopedagógico:</strong> através de um questionário individual e avaliação dos professores e pedagogos</li>
        <li><strong>IPV - Indicador do Ponto de Virada:</strong> através de um questionário individual e avaliação dos professores e pedagogos</li>
    </ul>
    <p>Esses 7 indicadores compõem o INDE - ÍNDICE DE DESENVOLVIMENTO EDUCACIONAL que, por sua vez está diretamente relacionado à classificação em pedras, de acordo com classificação:</p>
    <ul>
        <li><strong>Pedra-Conceito Quartzo:</strong> 3.302 ≤ INDE ≤ 6.109</li>
        <li><strong>Pedra-Conceito Ágata:</strong> 3.11 ≤ INDE ≤ 7.154</li>
        <li><strong>Pedra-Conceito Ametista:</strong> 7.154 ≤ INDE ≤ 8.198</li>
        <li><strong>Pedra-Conceito Topázio:</strong> 8.198 < INDE ≤ 9.442</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("""
    Dito isso, vamos analisar a distribuição de alunos em cada Pedra-Conceito por ano
                """)

  # Agrupar por 'PEDRA' e 'ANO' e contar o número de 'NOME'
    df_grouped = df_pm_not_nulls.groupby(['PEDRA', 'ANO']).size().reset_index(name='count')

    # Mapear as cores para tons pastéis válidos
    color_map = {
        '2020': 'thistle',
        '2021': 'lightblue',
        '2022': 'lavender'  # Cor alterada para uma cor válida
    }

    # Criar o gráfico de barras
    fig = px.bar(df_grouped, 
                x='PEDRA', 
                y='count',  # Usar a contagem de alunos como eixo Y
                color='ANO',  # Agrupa as barras por ano
                barmode='group',  # Exibe as barras agrupadas (em vez de empilhadas)
                title='Distribuição de Alunos por Classificação de Pedras e Ano', 
                labels={'PEDRA': 'Pedras', 'count': 'Qtdade Aluno'}, 
                category_orders={"PEDRA": df_grouped['PEDRA'].value_counts().index},
                color_discrete_map=color_map)

    # Atualizando o layout do gráfico
    fig.update_layout(
        xaxis_title='Pedras',
        yaxis_title='Qtdade Aluno',
        plot_bgcolor='white',  # Define o fundo do gráfico como branco
        yaxis=dict(showgrid=False),  # Remove as linhas de grade no eixo Y
        xaxis=dict(showgrid=False),  # Remove as linhas de grade no eixo X
        uniformtext_minsize=8,  # Tamanho mínimo do texto uniforme para os rótulos
        uniformtext_mode='show'  # Mostra todos os textos, mesmo que pequenos
    )

    # Adicionar rótulos de valor em cima das barras
    fig.update_traces(
        texttemplate='%{y:.0f}',  # Formata o valor de Y como inteiro sem casas decimais
        textposition='outside',  # Garante que os rótulos fiquem fora das barras
        textfont=dict(
            size=10,  # Tamanho da fonte dos rótulos
            color='black'  # Cor dos rótulos como preto
        )
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    Além disso, plotamos a evolução das pedras ao longo dos anos para facilitar o entendimento
                """)

    df_grouped = df_pm_not_nulls.groupby(['ANO', 'PEDRA']).size().reset_index(name='Quantidade')
    df_grouped['Porcentagem'] = df_grouped['Quantidade'] / df_grouped.groupby('ANO')['Quantidade'].transform('sum') * 100
    # Criando o gráfico de linha para mostrar a evolução da quantidade de alunos por pedra ao longo dos anos
    fig = px.line(df_grouped, 
              x='ANO', 
              y='Porcentagem', 
              color='PEDRA',  # Agrupa as linhas por tipo de pedra
              markers=True,  # Adiciona marcadores aos pontos de dados
              title='Porcentagem representativa de Alunos por Tipo de Pedra ao Longo dos Anos',
              labels={'ANO': 'Ano', 'Porcentagem': 'Porcentagem de Alunos', 'PEDRA': 'Tipo de Pedra'})

    # Atualizando o layout do gráfico
    fig.update_layout(
        xaxis_title='Ano',
        yaxis_title='Porcentagem de Alunos',
        legend_title_text='Tipo de Pedra',
        template='plotly',
        plot_bgcolor='white',  # Define o fundo do gráfico como branco
        yaxis=dict(showgrid=False),  # Remove as linhas de grade no eixo Y
        xaxis=dict(showgrid=False),  # Remove as linhas de grade no eixo X
    )

    # Atualizando as cores para tons pastéis
    fig.update_traces(line=dict(width=2), 
                    marker=dict(size=10),
                    marker_colorscale='Blues')

    # Adicionar rótulos de valor em cima dos marcadores
    fig.update_traces(
        texttemplate='%{y:.2f}%',  # Formata o valor de Y como percentual com 2 casas decimais
        textposition='top center',  # Posição dos rótulos acima dos marcadores
        textfont=dict(
            size=10,  # Tamanho da fonte dos rótulos
            color='black'  # Cor dos rótulos como preto
        ),
        mode='markers+text+lines'  # Exibe os marcadores, linhas e rótulos
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    st.write('# III. Construindo os Modelos')
    st.markdown("""
        Os modelos testados para ambas as previsões foram: **KNN, Random Forest e Support Vector Machine (SVM)**. Para cada um deles, avaliamos a acurácia para selecionar o modelo com melhor desempenho.       
                """)

    st.write('## A. Previsão de Ponto de Virada')
    st.markdown("""
    Para este primeiro modelo, utilizamos a base de dados para identificar quais dos indicadores mencionados acima apresentam maior correlação com o Ponto de Virada.""")

    #Ajustando os dados
    df_ponto_virada = df_pm_not_nulls[df_pm_not_nulls['PONTO_VIRADA'].isnull() == False]
    df_ponto_virada['PONTO_VIRADA_NUM'] = df_ponto_virada['PONTO_VIRADA'].map({'Sim': 1, 'Não': 0})
    colunas_numericas = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN', 'PONTO_VIRADA_NUM']
    df_numerico_pv = df_ponto_virada[colunas_numericas]
    matriz_correlacao = df_numerico_pv.corr()

    # Criando o heatmap com Plotly
    fig = go.Figure(data=go.Heatmap(
            z=matriz_correlacao.values,  # Valores da matriz de correlação
            x=matriz_correlacao.columns,  # Nomes das colunas
            y=matriz_correlacao.index,  # Nomes das linhas
            colorscale='Blues',  # Usando a paleta 'RdBu' que é similar ao 'coolwarm'
            zmid=0, 
            text=np.round(matriz_correlacao.values, 2),  # Adiciona os valores aos quadrados
            texttemplate="%{text}",  # Define que o texto mostrado será o valor
            hoverinfo="z", # Centraliza o gradiente de cores em 0
            colorbar=dict(title="Correlações")  # Adiciona um título à barra de cores
        ))

    fig.update_layout(
        title='Matriz de Correlação para Ponto de Virada',
        xaxis_nticks=36, 
        width=800,
        height=800
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    Embora alguns indicadores apresentem uma correlação maior com a nossa variável de saída, decidimos utilizar todos os indicadores como features independentes, uma vez que todas as correlações são positivas. A validação será feita com base na acurácia.
                """)

    st.write('#### Resultados de acurácia encontrados:')
    st.write("###### **- KNN**: 91.11%")
    st.write("###### **- Random Forest**: 96.22%")
    st.write("###### **- SVM**: 94.22%")

    st.markdown("""
    Como a acurácia dos modelos foi bastante alta, decidimos verificar a possibilidade de overfitting. Para isso, realizamos uma validação cruzada com 5 grupos diferentes dentro do mesmo dataset, medindo a média e o desvio padrão da acurácia""")
    
    st.write('#### Fazendo a validação cruzada, temos:')
    st.markdown("""
    <ul style="list-style-type: disc;">
        <li><strong>KNN</strong> - média acurácia: 92.3%, desvio padrão: 1.58% </li>
        <li><strong>Random Forest</strong> - média acurácia: 94.97%, desvio padrão: 2.15%</li>
        <li><strong>SVM</strong> - média acurácia: 95.01%, desvio padrão: 2.16%</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.write("""
    Como podemos ver, o modelo se comportou bem em todos os grupos de datasets distintos, mostrando que não está em overfiting. A escolha do modelo ideal para esse caso vai se dar pela maior precisão, mesmo significando um desvio padrão ligeiramente maior. 
    Por isso, escolhemos o modelo **SVM**.""")

    st.write('## B. Previsão de Indicação de Bolsa')
    st.markdown("""
    Para o próximo modelo, também utilizamos a base de dados para identificar quais dos indicadores mencionados acima apresentam maior correlação com o Ponto de Virada.""")

    df_indicado_bolsa = df_pm_not_nulls[df_pm_not_nulls['INDICADO_BOLSA'].isnull() == False]
    df_indicado_bolsa['INDICADO_BOLSA_NUM'] = df_indicado_bolsa['INDICADO_BOLSA'].map({'Sim': 1, 'Não': 0})
    colunas_numericas = ['INDE', 'IAA', 'IEG', 'IPS', 'IDA', 'IPP', 'IPV', 'IAN', 'INDICADO_BOLSA_NUM']
    df_numerico = df_indicado_bolsa[colunas_numericas]
    matriz_correlacao = df_numerico.corr()

    # Criando o heatmap com Plotly
    fig = go.Figure(data=go.Heatmap(
            z=matriz_correlacao.values,  # Valores da matriz de correlação
            x=matriz_correlacao.columns,  # Nomes das colunas
            y=matriz_correlacao.index,  # Nomes das linhas
            colorscale='RdBu',  
            zmid=0, 
            text=np.round(matriz_correlacao.values, 2),  # Adiciona os valores aos quadrados
            texttemplate="%{text}",  # Define que o texto mostrado será o valor
            hoverinfo="z", # Centraliza o gradiente de cores em 0
            colorbar=dict(title="Correlações")  # Adiciona um título à barra de cores
        ))

    fig.update_layout(
        title='Matriz de Correlação para Indicativo de Bolsa',
        xaxis_nticks=36, 
        width=800,
        height=800
    )

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    Para evitar as correlações negativas, vamos selecionar como variáveis independentes as duas features com maiores correlações: **IPP e IPV**.
                """)
    
    st.write('#### Resultados de acurácia e precisão encontrados:')
    st.markdown("""
    <ul style="list-style-type: disc;">
        <li><strong>KNN</strong> - acurácia: 78.03%, precisão: 78.72% </li>
        <li><strong>Random Forest</strong> - acurácia: 76.87%, precisão: 79.71%</li>
        <li><strong>SVM</strong> - acurácia: 75.72%, precisão: 85.26%</li>
    </ul>
    """, unsafe_allow_html=True)

    st.write("""
    Embora o modelo KNN tenha apresentado uma acurácia ligeiramente superior, observamos que o modelo SVM oferece uma precisão maior. Como a diferença na acurácia entre os dois modelos é insignificante, **optaremos pelo modelo SVM**, que proporciona um equilíbrio mais favorável entre precisão e desempenho geral.
                """)
    
    st.markdown("""
    <div style="text-align: center; color: red; font-size: 20px;">
        Para realizar previsões, selecione a página <strong>Deploy do Modelo</strong> no menu ao lado.
    </div>
""", unsafe_allow_html=True)


# Página de Deploy do Modelo
elif page == "Deploy do Modelo":

    st.write('### Fazer a previsão do Ponto de Virada')

    # Carregar o modelo treinado
    modelo = load('modelo_svm_pv.joblib')
    def fazer_previsao(inde, iaa, ieg, ips, ida, ipp, ipv, ian):
        # Cria um dataframe com as features
        dados = pd.DataFrame({
                    'INDE': [inde], 
                    'IAA': [iaa],
                    'IEG': [ieg],
                    'IPS': [ips],
                    'IDA': [ida],
                    'IPP': [ipp],
                    'IPV': [ipv],
                    'IAN': [ian]
                })
        # Faz a previsão
        previsao = modelo.predict(dados)
        return previsao[0]
    
    st.markdown("""
    <style>
    div[data-testid="stNumberInput"] {
        display: flex;
        align-items: flex-start; /* Alinhamento superior */
    }
    div[data-testid="stNumberInput"] > div {
        flex-grow: 1;
        display: flex;
        align-items: flex-start;
    }
    input[type="number"] {
        font-size: 18px !important;
        padding: 10px !important;
        height: 50px !important;
        width: calc(100% - 80px) !important; /* Ajusta a largura para incluir os botões */
        box-sizing: border-box;
        margin: 0px; /* Remover margens */
    }
    div[data-testid="stNumberInput"] button {
        font-size: 18px !important;
        padding: 10px !important;
        height: 50px !important;
        width: 40px !important;
        box-sizing: border-box;
    }
    div[data-testid="stNumberInput"] button:first-child {
        margin-right: -4px; /* Colar o botão de decremento ao input */
    }
    div[data-testid="stNumberInput"] button:last-child {
        margin-left: -4px; /* Colar o botão de incremento ao input */
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col5, col6, col7, col8 = st.columns(4)

    # Organizando as entradas nas colunas com number_input aceitando decimais
    with col1:
        inde_input = st.number_input(label="**:blue[INDE]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")
    with col2:
        ipp_input = st.number_input(label="**:blue[IPP]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")
    with col3:
        iaa_input = st.number_input(label="**:blue[IAA]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")
    with col4:
        ipv_input = st.number_input(label="**:blue[IPV]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")

    with col5:
        ieg_input = st.number_input(label="**:blue[IEG]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")
    with col6:
        ian_input = st.number_input(label="**:blue[IAN]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")
    with col7:
        ips_input = st.number_input(label="**:blue[IPS]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")
    with col8:
        ida_input = st.number_input(label="**:blue[IDA]**", min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f", label_visibility="visible")

    # Fazer a previsão
    if st.button('Fazer Previsão Ponto de Virada'):
        resultado = fazer_previsao(inde_input, iaa_input, ieg_input, ips_input, ida_input, ipp_input, ipv_input, ian_input)
        if resultado == 0:
            st.warning("⚠️ Ainda não está no ponto de virada")
        else:
            st.success("🎉 O aluno está pronto para o ponto de virada!")

    st.markdown('<div class="custom-hr"></div>', unsafe_allow_html=True)
    st.write('### Fazer a previsão do Indicativo de Bolsa')
    # Carregar o modelo treinado
    modelo = load('modelo_svm_b.joblib')
    def fazer_previsao_bolsa(ipp, ipv):
        # Cria um dataframe com as features
        dados = pd.DataFrame({
                    'IPV': [ipv],
                    'IPP': [ipp]
                })
        # Faz a previsão
        previsao = modelo.predict(dados)
        return previsao[0]
    
    col1, col2 = st.columns(2)

    with col1:
        ipv_input = st.number_input(label="**:orange[IPV]**",min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f")
    with col2:
        ipp_input = st.number_input(label="**:orange[IPP]**",min_value=0.0, max_value=10.0, value=0.0, step=0.1, format="%.1f")
    

    # Fazer a previsão
    if st.button('Fazer Previsão Indicação de Bolsa'):
        resultado = fazer_previsao_bolsa(ipp_input, ipv_input)
        if resultado == 0:
            st.warning("⚠️ Aluno ainda não recomendado para indicação de bolsa")
        else:
            st.success("🎉 O aluno está pronto para ser indicado para um bolsa!")