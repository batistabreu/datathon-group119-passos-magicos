# Análise e Previsibilidade de Desempenho - Alunos Passos Mágicos
Este repositório contém as entregas para o projeto de análise e previsibilidade de desempenho dos alunos da Associação Passos Mágicos. 

O objetivo deste trabalho é gerar insights de valor para a organização, além de criar modelos para auxiliar as tomadas de decisão:

## Sobre a Associação Passos Mágicos
A Associação Passos Mágicos dedica-se à transformação da vida de crianças e jovens de baixa renda da cidade de Embu-Guaçu desde 1992, proporcionando melhores oportunidades de vida para aqueles que mais precisam.

O projeto oferece educação de qualidade, apoio psicológico e psicopedagógico, além da promoção de uma visão ampliada do mundo e do protagonismo juvenil.
## - Dashboard no Power BI
O dashboard permite que gestores e educadores visualizem e analisem dados demográficos, desempenho acadêmico, frequência e outras métricas relevantes, proporcionando insights valiosos para a tomada de decisões.

## - Modelos de Machine Learning
### 1. Previsibilidade do Ponto de Virada
Este modelo visa prever se um aluno está prestes a alcançar um ponto de virada no seu desenvolvimento acadêmico e pessoal. Foram utilizadas várias métricas e indicadores para treinar este modelo, como:

- **INDE**: Índice de Desenvolvimento Educacional
- **IAA**: Indicador de Autoavaliação
- **IEG**: Indicador de Engajamento
- **IPS**: Indicador Psicossocial
- **IPP**: Indicador Psicopedagógico
- **IPV**: Indicador do Ponto de Virada
- **IAN**: Indicador de Adequação de Nível
- **IDA**: Indicador de Desempenho Acadêmico

### 2. Previsibilidade da Indicação para Bolsa de Estudos
Este modelo foi desenvolvido para prever se um aluno deve receber uma bolsa de estudos com base em nos indicadores **IPP** e **IPV**. 

### Interface de Usuário com Streamlit
O projeto inclui uma interface interativa desenvolvida com Streamlit, onde os usuários podem:

- Inserir os valores dos indicadores de desempenho de um aluno.
- Executar previsões para determinar se o aluno está pronto para o ponto de virada ou se deve ser indicado para uma bolsa de estudos.
